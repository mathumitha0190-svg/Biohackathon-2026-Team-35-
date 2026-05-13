from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from pcos_navigator.config import (
    DATA_PROFILE_PATH,
    MODEL_ARTIFACT_PATH,
    MODEL_REPORT_PATH,
    PROJECT_ROOT,
    READINESS_REPORT_PATH,
    REPORTS_DIR,
    SAFETY_STATEMENT,
)


REQUIRED_DOCS = [
    "docs/evidence_dossier.md",
    "docs/rubric_scorecard.md",
    "docs/limitations_and_validation.md",
    "docs/final_submission_checklist.md",
    "docs/demo_script.md",
    "docs/slide_outline.md",
    "docs/case_cards.md",
    "docs/judging_map.md",
]

GENERATED_ARTIFACTS = {
    "reports/data_profile.md": "uv run python scripts/profile_data.py",
    "reports/model_report.md": "uv run python scripts/train_models.py",
    "models/pcos_models.joblib": "uv run python scripts/train_models.py",
}

RUBRIC_CATEGORIES = [
    "Clinical & Scientific Validity",
    "Diagnostic Accuracy",
    "Feasibility & Implementation",
    "Innovation & Creativity",
    "Impact & Public Health Value",
    "Methodology and Scientific Rigor",
    "Code Quality & Technical Execution",
    "Presentation & Clarity",
]

BLOCKED_EXPORT_SUFFIXES = {".xlsx", ".csv", ".tar", ".joblib"}
EXPORT_DIR = PROJECT_ROOT / "exports" / "pcos_navigator_presentation"


@dataclass(frozen=True)
class ReadinessResult:
    label: str
    status: str
    detail: str


def check_required_docs(project_root: Path = PROJECT_ROOT) -> list[ReadinessResult]:
    results = []
    for relative_path in REQUIRED_DOCS:
        path = project_root / relative_path
        status = "PASS" if path.exists() else "FAIL"
        detail = "present" if path.exists() else "missing committed source doc"
        results.append(ReadinessResult(relative_path, status, detail))
    return results


def check_generated_artifacts(project_root: Path = PROJECT_ROOT) -> list[ReadinessResult]:
    results = []
    for relative_path, command in GENERATED_ARTIFACTS.items():
        path = project_root / relative_path
        if path.exists():
            results.append(ReadinessResult(relative_path, "PASS", "present"))
        else:
            results.append(
                ReadinessResult(
                    relative_path,
                    "WARN",
                    f"missing; regenerate with `{command}`",
                )
            )
    return results


def check_export_safety(export_dir: Path = EXPORT_DIR) -> list[ReadinessResult]:
    if not export_dir.exists():
        return [
            ReadinessResult(
                str(export_dir.relative_to(PROJECT_ROOT)),
                "WARN",
                "export missing; regenerate with `uv run python scripts/export_presentation.py`",
            )
        ]

    blocked = [
        path
        for path in export_dir.rglob("*")
        if path.is_file() and path.suffix.lower() in BLOCKED_EXPORT_SUFFIXES
    ]
    if blocked:
        names = ", ".join(str(path.relative_to(export_dir)) for path in blocked)
        return [ReadinessResult("export safety", "FAIL", f"blocked files found: {names}")]
    return [ReadinessResult("export safety", "PASS", "no datasets or model binaries found")]


def readiness_results(project_root: Path = PROJECT_ROOT, export_dir: Path = EXPORT_DIR) -> list[ReadinessResult]:
    return [
        *check_required_docs(project_root),
        *check_generated_artifacts(project_root),
        *check_export_safety(export_dir),
    ]


def readiness_to_markdown(results: list[ReadinessResult]) -> str:
    lines = [
        "# PCOS Navigator Readiness Report",
        "",
        f"> {SAFETY_STATEMENT}",
        "",
        "## App Command",
        "",
        "```powershell",
        "uv run streamlit run app.py",
        "```",
        "",
        "## Rubric Categories Covered",
        "",
    ]
    lines.extend(f"- {category}" for category in RUBRIC_CATEGORIES)
    lines.extend(
        [
            "",
            "## Readiness Checks",
            "",
            "| Item | Status | Detail |",
            "|---|---|---|",
        ]
    )
    for result in results:
        lines.append(f"| `{result.label}` | {result.status} | {result.detail} |")

    lines.extend(
        [
            "",
            "## Recommended Final Sequence",
            "",
            "```powershell",
            "uv run python scripts/profile_data.py",
            "uv run python scripts/train_models.py",
            "uv run python scripts/check_readiness.py",
            "uv run python scripts/export_presentation.py",
            "uv run pytest",
            "uv run streamlit run app.py",
            "```",
        ]
    )
    return "\n".join(lines) + "\n"


def write_readiness_report(path: Path = READINESS_REPORT_PATH) -> Path:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    results = readiness_results()
    path.write_text(readiness_to_markdown(results), encoding="utf-8")
    return path


def main() -> None:
    report_path = write_readiness_report()
    print(f"Wrote {report_path}")


if __name__ == "__main__":
    main()
