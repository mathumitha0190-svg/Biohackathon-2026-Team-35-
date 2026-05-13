from __future__ import annotations

import shutil
from pathlib import Path

from pcos_navigator.config import MODEL_REPORT_PATH, PROJECT_ROOT, READINESS_REPORT_PATH, SAFETY_STATEMENT


DOC_FILENAMES = [
    "demo_script.md",
    "slide_outline.md",
    "case_cards.md",
    "judging_map.md",
    "evidence_dossier.md",
    "rubric_scorecard.md",
    "limitations_and_validation.md",
    "final_submission_checklist.md",
]

SOURCE_DOCS_DIR = PROJECT_ROOT / "docs"
EXPORT_ROOT = PROJECT_ROOT / "exports"
EXPORT_DIR = EXPORT_ROOT / "pcos_navigator_presentation"

BLOCKED_SUFFIXES = {".xlsx", ".csv", ".tar", ".joblib"}


def build_export_readme(includes_model_report: bool, includes_readiness_report: bool) -> str:
    model_report_line = (
        "- `model_report.md`: generated model evidence summary\n"
        if includes_model_report
        else "- `model_report.md`: not included because it has not been generated yet\n"
    )
    readiness_report_line = (
        "- `readiness_report.md`: generated final readiness checks\n"
        if includes_readiness_report
        else "- `readiness_report.md`: not included because it has not been generated yet\n"
    )
    return (
        "# PCOS Navigator Presentation Bundle\n\n"
        f"> {SAFETY_STATEMENT}\n\n"
        "## Recommended Demo Order\n\n"
        "1. Typical PCOS\n"
        "2. Lean PCOS\n"
        "3. Endometriosis-like\n"
        "4. Incomplete Data\n\n"
        "## Run Commands\n\n"
        "```powershell\n"
        "uv run python scripts/profile_data.py\n"
        "uv run python scripts/train_models.py\n"
        "uv run python scripts/check_readiness.py\n"
        "uv run streamlit run app.py\n"
        "```\n\n"
        "Open the app at:\n\n"
        "```text\n"
        "http://localhost:8501\n"
        "```\n\n"
        "## Included Files\n\n"
        "- `demo_script.md`: 5-minute live demo path\n"
        "- `slide_outline.md`: 8-slide pitch structure\n"
        "- `case_cards.md`: prepared patient demo cases\n"
        "- `judging_map.md`: rubric mapping\n"
        "- `evidence_dossier.md`: cited clinical rationale\n"
        "- `rubric_scorecard.md`: full rubric proof checklist\n"
        "- `limitations_and_validation.md`: validation caveats and deployment plan\n"
        "- `final_submission_checklist.md`: pre-demo checklist\n"
        f"{model_report_line}\n"
        f"{readiness_report_line}\n"
        "This export intentionally excludes datasets and model binaries.\n"
    )


def ensure_no_blocked_files(export_dir: Path = EXPORT_DIR) -> None:
    blocked = [
        path
        for path in export_dir.rglob("*")
        if path.is_file() and path.suffix.lower() in BLOCKED_SUFFIXES
    ]
    if blocked:
        names = ", ".join(str(path.relative_to(export_dir)) for path in blocked)
        raise RuntimeError(f"Export contains blocked files: {names}")


def export_presentation(export_dir: Path = EXPORT_DIR) -> Path:
    if export_dir.exists():
        shutil.rmtree(export_dir)
    export_dir.mkdir(parents=True, exist_ok=True)

    for filename in DOC_FILENAMES:
        source = SOURCE_DOCS_DIR / filename
        if not source.exists():
            raise FileNotFoundError(f"Missing presentation doc: {source}")
        shutil.copy2(source, export_dir / filename)

    includes_model_report = MODEL_REPORT_PATH.exists()
    if includes_model_report:
        shutil.copy2(MODEL_REPORT_PATH, export_dir / "model_report.md")

    includes_readiness_report = READINESS_REPORT_PATH.exists()
    if includes_readiness_report:
        shutil.copy2(READINESS_REPORT_PATH, export_dir / "readiness_report.md")

    (export_dir / "README.md").write_text(
        build_export_readme(includes_model_report, includes_readiness_report),
        encoding="utf-8",
    )
    ensure_no_blocked_files(export_dir)
    return export_dir


def main() -> None:
    export_dir = export_presentation()
    print(f"Wrote presentation export: {export_dir}")


if __name__ == "__main__":
    main()
