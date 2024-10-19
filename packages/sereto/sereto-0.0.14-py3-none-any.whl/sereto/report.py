import importlib.metadata
from collections.abc import Callable
from functools import wraps
from pathlib import Path
from shutil import copy2, copytree
from typing import TypeVar

from click import get_current_context
from pydantic import validate_call
from rich.prompt import Prompt
from typing_extensions import ParamSpec

from sereto.cleanup import render_finding_group_cleanup, render_report_cleanup, render_target_cleanup
from sereto.cli.utils import Console
from sereto.exceptions import SeretoPathError, SeretoValueError
from sereto.finding import render_finding_group_j2
from sereto.jinja import render_j2
from sereto.models.config import Config
from sereto.models.report import Report
from sereto.models.settings import Settings
from sereto.models.version import ReportVersion, SeretoVersion
from sereto.pdf import render_finding_group_pdf, render_report_pdf, render_target_pdf
from sereto.plot import risks_plot
from sereto.source_archive import create_source_archive, embed_source_archive
from sereto.target import create_findings_config, get_risks, render_target_j2  # render_target_findings_j2
from sereto.types import TypeReportId

P = ParamSpec("P")
R = TypeVar("R")


def load_report(f: Callable[..., R]) -> Callable[..., R]:
    """Decorator which calls `load_report_function` and provides Report as the first argument"""

    @wraps(f)
    def wrapper(settings: Settings, *args: P.args, **kwargs: P.kwargs) -> R:
        report = load_report_function(settings=settings)
        report.load_runtime_vars(settings=settings)
        return get_current_context().invoke(f, report, settings, *args, **kwargs)

    return wrapper


def load_report_function(settings: Settings, report_path: Path | None = None) -> Report:
    config_path = (
        Report.get_config_path(dir_subtree=settings.reports_path)
        if report_path is None
        else report_path / "config.json"
    )
    config = Config.from_file(filepath=config_path)
    return Report(config=config)


def get_all_reports(settings: Settings) -> list[Report]:
    report_paths: list[Path] = [d for d in settings.reports_path.iterdir() if Report.is_report_dir(d)]
    return [load_report_function(settings=settings, report_path=d) for d in report_paths]


def get_all_reports_dict(settings: Settings) -> dict[str, Report]:
    report_paths: list[Path] = [d for d in settings.reports_path.iterdir() if Report.is_report_dir(d)]
    return {(report := load_report_function(settings=settings, report_path=d)).config.id: report for d in report_paths}


@validate_call
def copy_skel(templates: Path, dst: Path, overwrite: bool = False) -> None:
    """Copy the content of a templates `skel` directory to a destination directory.

    A `skel` directory is a directory that contains a set of files and directories that can be used as a template
    for creating new projects. This function copies the contents of the `skel` directory located at
    the path specified by `templates` to the destination directory specified by `dst`.

    Args:
        templates: The path to the directory containing the `skel` directory.
        dst: The destination directory to copy the `skel` directory contents to.
        overwrite: Whether to allow overwriting of existing files in the destination directory.
            If `True`, existing files will be overwritten. If `False` (default), a `SeretoPathError` will be raised
            if the destination directory already exists.

    Raises:
        SeretoPathError: If the destination directory already exists and `overwrite` is `False`.
    """
    skel_path: Path = templates / "skel"
    Console().log(f"Copying 'skel' directory: '{skel_path}' -> '{dst}'")

    for item in skel_path.iterdir():
        dst_item: Path = dst / (item.relative_to(skel_path))
        if not overwrite and dst_item.exists():
            raise SeretoPathError("Destination already exists")
        if item.is_file():
            Console().log(f" [green]+[/green] copy file: '{item.relative_to(skel_path)}'")
            copy2(item, dst_item, follow_symlinks=False)
        if item.is_dir():
            Console().log(f" [green]+[/green] copy dir: '{item.relative_to(skel_path)}'")
            copytree(item, dst_item, dirs_exist_ok=overwrite)


@validate_call
def new_report(
    settings: Settings,
    report_id: TypeReportId,
) -> None:
    """Generates a new report with the specified ID.

    Args:
        settings: Global settings.
        report_id: The ID of the new report. This should be a string that uniquely identifies the report.

    Raises:
        SeretoValueError: If a report with the specified ID already exists in the `reports` directory.
    """
    Console().log(f"Generating a new report with ID {report_id!r}")

    if (new_path := (settings.reports_path / report_id)).exists():
        raise SeretoValueError("report with specified ID already exists")
    else:
        new_path.mkdir()

    Console().print("[cyan]We will ask you a few questions to set up the new report.\n")

    report_name: str = Prompt.ask("Name of the report", console=Console())
    sereto_ver = importlib.metadata.version("sereto")

    cfg = Config(
        sereto_version=SeretoVersion.from_str(sereto_ver),
        id=report_id,
        name=report_name,
        report_version=ReportVersion.from_str("v1.0"),
    )

    Console().log("Copy report skeleton")
    copy_skel(templates=settings.templates_path, dst=new_path)

    config_path: Path = new_path / "config.json"
    Console().log(f"Writing the config '{config_path}'")
    with config_path.open("w", encoding="utf-8") as f:
        f.write(cfg.model_dump_json(indent=2))


@validate_call
def render_report_j2(
    report: Report,
    settings: Settings,
    version: ReportVersion,
    convert_recipe: str | None = None,
) -> None:
    """Renders Jinja templates into TeX files.

    This function processes Jinja templates for report, approach and scope in each target, and all relevant findings.

    Args:
        report: Report's representation.
        settings: Global settings.
        version: The version of the report which should be rendered.
        convert_recipe: Name which will be used to pick a recipe from Render configuration. If none is provided, the
            first recipe with a matching format is used.
    """
    cfg = report.config.at_version(version=version)
    report_path = Report.get_path_from_cwd(dir_subtree=settings.reports_path)

    for target in cfg.targets:
        # render_target_findings_j2(target=target, settings=settings, version=version, convert_recipe=convert_recipe)
        render_target_j2(
            target=target, report=report, settings=settings, version=version, convert_recipe=convert_recipe
        )

        for finding_group in target.findings_config.finding_groups:
            render_finding_group_j2(
                finding_group=finding_group, target=target, report=report, settings=settings, version=version
            )

    report_j2_path = report_path / f"report{version.path_suffix}.tex.j2"
    if not report_j2_path.is_file():
        raise SeretoPathError(f"template not found: '{report_j2_path}'")

    # make shallow dict - values remain objects on which we can call their methods in Jinja
    cfg_dict = {key: getattr(cfg, key) for key in cfg.model_dump()}
    report_generator = render_j2(
        templates=report_path,
        file=report_j2_path,
        vars={"version": version, "report_path": report_path, **cfg_dict},
    )

    with report_j2_path.with_suffix("").open("w", encoding="utf-8") as f:
        for chunk in report_generator:
            f.write(chunk)
        Console().log(f"Rendered Jinja template: {report_j2_path.with_suffix('').relative_to(report_path)}")


@validate_call
def render_sow_j2(report: Report, settings: Settings, version: ReportVersion) -> None:
    cfg = report.config.at_version(version=version)
    report_path = Report.get_path_from_cwd(dir_subtree=settings.reports_path)

    sow_j2_path = report_path / f"sow{version.path_suffix}.tex.j2"
    if not sow_j2_path.is_file():
        raise SeretoPathError(f"template not found: '{sow_j2_path}'")

    with sow_j2_path.with_suffix("").open("w", encoding="utf-8") as f:
        # make shallow dict - values remain objects on which we can call their methods in Jinja
        cfg_dict = {key: getattr(cfg, key) for key in cfg.model_dump()}
        sow_generator = render_j2(
            templates=report_path,
            file=sow_j2_path,
            vars={"version": version, "report_path": report_path, **cfg_dict},
        )
        for chunk in sow_generator:
            f.write(chunk)
        Console().log(f"Rendered Jinja template: {sow_j2_path.with_suffix('').relative_to(report_path)}")


@validate_call
def report_create_missing(report: Report, settings: Settings, version: ReportVersion) -> None:
    """Creates missing target directories from config.

    This function creates any missing target directories and populates them with content of the "skel" directory from
    templates.

    Args:
        report: Report's representation.
        settings: Global settings.
        version: The version of the report.
    """
    cfg = report.config.at_version(version=version)

    for target in cfg.targets:
        assert target.path is not None
        category_templates = settings.templates_path / "categories" / target.category

        if not target.path.is_dir():
            Console().log(f"Target directory not found, creating: '{target.path}'")
            target.path.mkdir()
            if (category_templates / "skel").is_dir():
                Console().log(f"""Populating new target directory from: '{category_templates / "skel"}'""")
                copy_skel(templates=category_templates, dst=target.path)
            else:
                Console().log(f"No 'skel' directory found: '{category_templates}'")

            create_findings_config(target=target, report=report, templates=category_templates / "findings")

        risks = get_risks(target=target, version=version)
        risks_plot(risks=risks, path=target.path / "risks.png")

        for finding_group in target.findings_config.finding_groups:
            finding_group_j2_path = target.path / "findings" / f"{finding_group.uname}.tex.j2"
            if not finding_group_j2_path.is_file():
                copy2(category_templates / "finding_group.tex.j2", finding_group_j2_path, follow_symlinks=False)


@validate_call
def report_pdf(
    report: Report,
    settings: Settings,
    version: ReportVersion,
    report_recipe: str | None = None,
    target_recipe: str | None = None,
    finding_recipe: str | None = None,
) -> None:
    cfg = report.config.at_version(version=version)

    for target in cfg.targets:
        render_target_pdf(target=target, report=report, settings=settings, version=version, recipe=target_recipe)

        for finding_group in target.findings_config.finding_groups:
            render_finding_group_pdf(
                finding_group=finding_group,
                target=target,
                report=report,
                settings=settings,
                version=version,
                recipe=finding_recipe,
            )

    report_path = render_report_pdf(settings=settings, version=version, recipe=report_recipe)
    archive_path = create_source_archive(settings=settings)
    embed_source_archive(archive=archive_path, report=report_path, keep_original=False)


@validate_call
def report_cleanup(
    report: Report,
    settings: Settings,
    version: ReportVersion,
) -> None:
    cfg = report.config.at_version(version=version)

    for target in cfg.targets:
        render_target_cleanup(target=target, settings=settings)

        for finding_group in target.findings_config.finding_groups:
            render_finding_group_cleanup(
                finding_group=finding_group,
                target=target,
                settings=settings,
            )

    render_report_cleanup(settings=settings, version=version)
