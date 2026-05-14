from __future__ import annotations

import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from pcos_navigator.config import (
    DATA_PROFILE_PATH,
    MODEL_ARTIFACT_PATH,
    MODEL_METRICS_PATH,
    MODEL_REPORT_PATH,
    PREFLIGHT_REPORT_PATH,
    PROJECT_ROOT,
    READINESS_REPORT_PATH,
    REPORTS_DIR,
    SAFETY_STATEMENT,
    VISUAL_EVIDENCE_REPORT_PATH,
)
from scripts.check_visual_evidence import VisualEvidenceResult, check_visual_evidence
from scripts.export_presentation import BLOCKED_SUFFIXES, EXPORT_DIR, export_presentation


COMMAND_TIMEOUT_SECONDS = 900


@dataclass(frozen=True)
class CommandSpec:
    label: str
    display: str
    args: tuple[str, ...]


@dataclass(frozen=True)
class CommandResult:
    label: str
    command: str
    status: str
    returncode: int | None
    detail: str


@dataclass(frozen=True)
class CheckResult:
    label: str
    status: str
    detail: str


PREFLIGHT_COMMANDS = [
    CommandSpec(
        "Data profile",
        "uv run python scripts/profile_data.py",
        ("uv", "run", "python", "scripts/profile_data.py"),
    ),
    CommandSpec(
        "Model training and reports",
        "uv run python scripts/train_models.py",
        ("uv", "run", "python", "scripts/train_models.py"),
    ),
    CommandSpec(
        "Readiness report",
        "uv run python scripts/check_readiness.py",
        ("uv", "run", "python", "scripts/check_readiness.py"),
    ),
    CommandSpec(
        "Visual evidence report",
        "uv run python scripts/check_visual_evidence.py",
        ("uv", "run", "python", "scripts/check_visual_evidence.py"),
    ),
    CommandSpec(
        "Presentation export",
        "uv run python scripts/export_presentation.py",
        ("uv", "run", "python", "scripts/export_presentation.py"),
    ),
    CommandSpec("Test suite", "uv run pytest", ("uv", "run", "pytest")),
    CommandSpec(
        "App import",
        'uv run python -c "import app; print(\'app import ok\')"',
        ("uv", "run", "python", "-c", "import app; print('app import ok')"),
    ),
]

GENERATED_ARTIFACTS = {
    "reports/data_profile.md": (
        DATA_PROFILE_PATH,
        "uv run python scripts/profile_data.py",
    ),
    "reports/model_metrics.json": (
        MODEL_METRICS_PATH,
        "uv run python scripts/train_models.py",
    ),
    "reports/model_report.md": (
        MODEL_REPORT_PATH,
        "uv run python scripts/train_models.py",
    ),
    "reports/readiness_report.md": (
        READINESS_REPORT_PATH,
        "uv run python scripts/check_readiness.py",
    ),
    "reports/visual_evidence_report.md": (
        VISUAL_EVIDENCE_REPORT_PATH,
        "uv run python scripts/check_visual_evidence.py",
    ),
    "reports/preflight_submission_report.md": (
        PREFLIGHT_REPORT_PATH,
        "uv run python scripts/preflight_submission.py",
    ),
    "models/pcos_models.joblib": (
        MODEL_ARTIFACT_PATH,
        "uv run python scripts/train_models.py",
    ),
    "exports/pcos_navigator_presentation/": (
        EXPORT_DIR,
        "uv run python scripts/export_presentation.py",
    ),
}

DEMO_ORDER = [
    "Typical PCOS",
    "Lean PCOS",
    "Endometriosis-like",
    "Incomplete Data",
    "Model Evidence",
]

RUBRIC_EVIDENCE = [
    "Clinical validity: guideline checklist, exclusion gaps, and cited evidence dossier",
    "Diagnostic accuracy: tier metrics, confidence intervals, calibration, and thresholds",
    "Feasibility: Streamlit demo, uv workflow, export bundle, and reproducible scripts",
    "Innovation and impact: resource-tiered PCOS triage plus endometriosis red-flag handoff",
    "Methodology: dataset audit, subgroup caveats, and generated model report",
    "Code quality and presentation: tests, readiness checks, docs, and visual evidence guide",
]


def _trim_output(value: str, max_chars: int = 500) -> str:
    normalized = " ".join(value.strip().split())
    if len(normalized) <= max_chars:
        return normalized
    return f"{normalized[-max_chars:]}".strip()


def _cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def run_preflight_command(
    command: CommandSpec,
    project_root: Path = PROJECT_ROOT,
    timeout_seconds: int = COMMAND_TIMEOUT_SECONDS,
) -> CommandResult:
    started = time.perf_counter()
    try:
        completed = subprocess.run(
            command.args,
            cwd=project_root,
            text=True,
            capture_output=True,
            timeout=timeout_seconds,
            check=False,
        )
    except FileNotFoundError as exc:
        return CommandResult(command.label, command.display, "FAIL", None, f"command not found: {exc}")
    except subprocess.TimeoutExpired as exc:
        detail = _trim_output(exc.stderr or exc.stdout or "")
        suffix = f"; output: {detail}" if detail else ""
        return CommandResult(command.label, command.display, "FAIL", None, f"timed out after {timeout_seconds}s{suffix}")

    elapsed = time.perf_counter() - started
    if completed.returncode == 0:
        return CommandResult(
            command.label,
            command.display,
            "PASS",
            completed.returncode,
            f"completed in {elapsed:.1f}s",
        )

    detail = _trim_output(completed.stderr or completed.stdout)
    if not detail:
        detail = "no output captured"
    return CommandResult(
        command.label,
        command.display,
        "FAIL",
        completed.returncode,
        f"failed in {elapsed:.1f}s: {detail}",
    )


def run_preflight_commands(commands: list[CommandSpec] | None = None) -> list[CommandResult]:
    return [run_preflight_command(command) for command in (commands or PREFLIGHT_COMMANDS)]


def check_generated_artifacts(project_root: Path = PROJECT_ROOT) -> list[CheckResult]:
    results = []
    for label, (path, command) in GENERATED_ARTIFACTS.items():
        resolved = project_root / path.relative_to(PROJECT_ROOT) if path.is_absolute() else project_root / path
        if resolved.exists():
            detail = "present"
            if resolved.is_dir():
                file_count = len([item for item in resolved.rglob("*") if item.is_file()])
                detail = f"present with {file_count} files"
            results.append(CheckResult(label, "PASS", detail))
        else:
            results.append(CheckResult(label, "FAIL", f"missing; regenerate with `{command}`"))
    return results


def summarize_export_bundle(export_dir: Path = EXPORT_DIR) -> list[CheckResult]:
    if not export_dir.exists():
        return [
            CheckResult(
                str(export_dir.relative_to(PROJECT_ROOT)),
                "FAIL",
                "missing; regenerate with `uv run python scripts/export_presentation.py`",
            )
        ]

    exported_files = sorted(path for path in export_dir.rglob("*") if path.is_file())
    blocked = [path for path in exported_files if path.suffix.lower() in BLOCKED_SUFFIXES]
    markdown_files = [str(path.relative_to(export_dir)) for path in exported_files if path.suffix.lower() == ".md"]
    screenshot_files = [str(path.relative_to(export_dir)) for path in exported_files if path.suffix.lower() == ".png"]

    return [
        CheckResult("export folder", "PASS", f"{len(exported_files)} files exported"),
        CheckResult(
            "export blocked files",
            "FAIL" if blocked else "PASS",
            ", ".join(str(path.relative_to(export_dir)) for path in blocked) if blocked else "none found",
        ),
        CheckResult(
            "export markdown files",
            "PASS" if markdown_files else "WARN",
            ", ".join(markdown_files) if markdown_files else "none found",
        ),
        CheckResult(
            "export screenshots",
            "PASS" if screenshot_files else "WARN",
            ", ".join(screenshot_files) if screenshot_files else "no screenshots exported",
        ),
    ]


def command_results_to_markdown(results: list[CommandResult]) -> list[str]:
    lines = [
        "| Step | Command | Status | Return code | Detail |",
        "|---|---|---|---|---|",
    ]
    for result in results:
        returncode = "" if result.returncode is None else result.returncode
        lines.append(
            f"| {_cell(result.label)} | `{_cell(result.command)}` | {result.status} | {_cell(returncode)} | {_cell(result.detail)} |"
        )
    return lines


def check_results_to_markdown(results: list[CheckResult]) -> list[str]:
    lines = [
        "| Item | Status | Detail |",
        "|---|---|---|",
    ]
    for result in results:
        lines.append(f"| `{_cell(result.label)}` | {result.status} | {_cell(result.detail)} |")
    return lines


def screenshot_results_to_markdown(results: list[VisualEvidenceResult]) -> list[str]:
    lines = [
        "| Screenshot | Status | Rubric purpose | Detail |",
        "|---|---|---|---|",
    ]
    for result in results:
        lines.append(
            f"| `{_cell(result.filename)}` | {result.status} | {_cell(result.rubric)} | {_cell(result.detail)} |"
        )
    return lines


def preflight_to_markdown(
    command_results: list[CommandResult],
    artifact_results: list[CheckResult],
    export_results: list[CheckResult],
    screenshot_results: list[VisualEvidenceResult],
) -> str:
    lines = [
        "# PCOS Navigator Preflight Submission Report",
        "",
        f"> {SAFETY_STATEMENT}",
        "",
        f"Generated: {datetime.now(UTC).isoformat(timespec='seconds')}",
        "",
        "## App Command",
        "",
        "```powershell",
        "uv run streamlit run app.py",
        "```",
        "",
        "## Command Results",
        "",
        *command_results_to_markdown(command_results),
        "",
        "## Generated Artifact Checklist",
        "",
        *check_results_to_markdown(artifact_results),
        "",
        "## Export Bundle Summary",
        "",
        *check_results_to_markdown(export_results),
        "",
        "## Screenshot Evidence Status",
        "",
        "Missing screenshots are warnings, not failures.",
        "",
        *screenshot_results_to_markdown(screenshot_results),
        "",
        "## Final Demo Order",
        "",
    ]
    lines.extend(f"{index}. {case}" for index, case in enumerate(DEMO_ORDER, start=1))
    lines.extend(
        [
            "",
            "## Rubric-Facing Evidence",
            "",
        ]
    )
    lines.extend(f"- {item}" for item in RUBRIC_EVIDENCE)
    return "\n".join(lines) + "\n"


def has_failures(command_results: list[CommandResult], artifact_results: list[CheckResult], export_results: list[CheckResult]) -> bool:
    return any(result.status == "FAIL" for result in [*command_results, *artifact_results, *export_results])


def write_preflight_report(path: Path = PREFLIGHT_REPORT_PATH) -> tuple[Path, bool]:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    command_results = run_preflight_commands()

    artifact_results = check_generated_artifacts()
    export_results = summarize_export_bundle()
    screenshot_results = check_visual_evidence()
    path.write_text(
        preflight_to_markdown(command_results, artifact_results, export_results, screenshot_results),
        encoding="utf-8",
    )

    export_command_passed = any(
        result.label == "Presentation export" and result.status == "PASS"
        for result in command_results
    )
    if export_command_passed:
        export_presentation()
        artifact_results = check_generated_artifacts()
        export_results = summarize_export_bundle()
        path.write_text(
            preflight_to_markdown(command_results, artifact_results, export_results, screenshot_results),
            encoding="utf-8",
        )
        shutil.copy2(path, EXPORT_DIR / path.name)

    return path, has_failures(command_results, artifact_results, export_results)


def main() -> None:
    report_path, failed = write_preflight_report()
    print(f"Wrote {report_path}")
    raise SystemExit(1 if failed else 0)


if __name__ == "__main__":
    main()
