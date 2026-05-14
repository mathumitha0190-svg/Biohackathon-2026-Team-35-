from __future__ import annotations

import shutil
from pathlib import Path

from pcos_navigator.config import (
    MODEL_REPORT_PATH,
    PREFLIGHT_REPORT_PATH,
    PROJECT_ROOT,
    READINESS_REPORT_PATH,
    SAFETY_STATEMENT,
    SCREENSHOTS_DIR,
    VISUAL_EVIDENCE_REPORT_PATH,
)


DOC_FILENAMES = [
    "demo_script.md",
    "slide_outline.md",
    "case_cards.md",
    "judging_map.md",
    "evidence_dossier.md",
    "rubric_scorecard.md",
    "limitations_and_validation.md",
    "final_submission_checklist.md",
    "visual_evidence_guide.md",
    "final_demo_rehearsal.md",
]

SOURCE_DOCS_DIR = PROJECT_ROOT / "docs"
EXPORT_ROOT = PROJECT_ROOT / "exports"
EXPORT_DIR = EXPORT_ROOT / "pcos_navigator_presentation"

BLOCKED_SUFFIXES = {".xlsx", ".csv", ".tar", ".joblib"}


def build_export_readme(
    includes_model_report: bool,
    includes_readiness_report: bool,
    includes_visual_report: bool,
    includes_preflight_report: bool,
) -> str:
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
    visual_report_line = (
        "- `visual_evidence_report.md`: generated screenshot readiness checks\n"
        if includes_visual_report
        else "- `visual_evidence_report.md`: not included because it has not been generated yet\n"
    )
    preflight_report_line = (
        "- `preflight_submission_report.md`: generated final judge dry-run report\n"
        if includes_preflight_report
        else "- `preflight_submission_report.md`: not included because it has not been generated yet\n"
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
        "uv run python scripts/check_visual_evidence.py\n"
        "uv run streamlit run app.py\n"
        "```\n\n"
        "One-command pre-demo dry run:\n\n"
        "```powershell\n"
        "uv run python scripts/preflight_submission.py\n"
        "```\n\n"
        "Strict screenshot gate after images are captured:\n\n"
        "```powershell\n"
        "uv run python scripts/preflight_submission.py --strict-screenshots\n"
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
        "- `visual_evidence_guide.md`: screenshot capture guide\n"
        "- `final_demo_rehearsal.md`: timed demo rehearsal plan\n"
        f"{model_report_line}\n"
        f"{readiness_report_line}\n"
        f"{visual_report_line}\n"
        f"{preflight_report_line}\n"
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

    includes_visual_report = VISUAL_EVIDENCE_REPORT_PATH.exists()
    if includes_visual_report:
        shutil.copy2(VISUAL_EVIDENCE_REPORT_PATH, export_dir / "visual_evidence_report.md")

    includes_preflight_report = PREFLIGHT_REPORT_PATH.exists()
    if includes_preflight_report:
        shutil.copy2(PREFLIGHT_REPORT_PATH, export_dir / "preflight_submission_report.md")

    screenshots = [
        path for path in SCREENSHOTS_DIR.glob("*.png")
        if path.is_file()
    ]
    if screenshots:
        screenshots_export_dir = export_dir / "screenshots"
        screenshots_export_dir.mkdir(parents=True, exist_ok=True)
        for screenshot in screenshots:
            shutil.copy2(screenshot, screenshots_export_dir / screenshot.name)

    (export_dir / "README.md").write_text(
        build_export_readme(
            includes_model_report,
            includes_readiness_report,
            includes_visual_report,
            includes_preflight_report,
        ),
        encoding="utf-8",
    )
    ensure_no_blocked_files(export_dir)
    return export_dir


def main() -> None:
    export_dir = export_presentation()
    print(f"Wrote presentation export: {export_dir}")


if __name__ == "__main__":
    main()
