from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from pcos_navigator.config import (
    REPORTS_DIR,
    SAFETY_STATEMENT,
    SCREENSHOTS_DIR,
    VISUAL_EVIDENCE_REPORT_PATH,
)


EXPECTED_SCREENSHOTS = [
    {
        "filename": "01_intake_summary.png",
        "purpose": "Shows sidebar demo path, why-case text, intake, and top summary row.",
        "rubric": "Feasibility, presentation clarity",
    },
    {
        "filename": "02_risk_result.png",
        "purpose": "Shows triage risk, probability gauge, confidence, and coefficient drivers.",
        "rubric": "Diagnostic accuracy, interpretability",
    },
    {
        "filename": "03_guideline_checklist.png",
        "purpose": "Shows guideline checklist statuses and evidence table.",
        "rubric": "Clinical and scientific validity",
    },
    {
        "filename": "04_model_evidence.png",
        "purpose": "Shows model metrics, calibration, threshold tradeoff, and subgroup summary.",
        "rubric": "Methodology, validation rigor",
    },
    {
        "filename": "05_next_action_handoff.png",
        "purpose": "Shows grouped actions, differential flags, missing evidence, and handoff summary.",
        "rubric": "Innovation, clinical workflow value",
    },
    {
        "filename": "06_readiness_export.png",
        "purpose": "Shows readiness report or export bundle contents.",
        "rubric": "Code quality, reproducibility, presentation readiness",
    },
]


@dataclass(frozen=True)
class VisualEvidenceResult:
    filename: str
    status: str
    purpose: str
    rubric: str
    detail: str


def check_visual_evidence(screenshots_dir: Path = SCREENSHOTS_DIR) -> list[VisualEvidenceResult]:
    results = []
    for item in EXPECTED_SCREENSHOTS:
        path = screenshots_dir / item["filename"]
        exists = path.exists()
        results.append(
            VisualEvidenceResult(
                filename=item["filename"],
                status="PASS" if exists else "WARN",
                purpose=item["purpose"],
                rubric=item["rubric"],
                detail="present" if exists else f"missing; capture and save to `{path}`",
            )
        )
    return results


def visual_evidence_to_markdown(results: list[VisualEvidenceResult]) -> str:
    lines = [
        "# PCOS Navigator Visual Evidence Report",
        "",
        f"> {SAFETY_STATEMENT}",
        "",
        "Screenshots are optional but recommended for judges and slides. Missing screenshots are warnings, not failures.",
        "",
        "## Screenshot Checks",
        "",
        "| Screenshot | Status | Rubric purpose | What it proves | Detail |",
        "|---|---|---|---|---|",
    ]
    for result in results:
        lines.append(
            f"| `{result.filename}` | {result.status} | {result.rubric} | {result.purpose} | {result.detail} |"
        )
    lines.extend(
        [
            "",
            "## Capture Command Flow",
            "",
            "```powershell",
            "uv run python scripts/profile_data.py",
            "uv run python scripts/train_models.py",
            "uv run python scripts/check_readiness.py",
            "uv run python scripts/export_presentation.py",
            "uv run streamlit run app.py",
            "```",
            "",
            "See `docs/visual_evidence_guide.md` for exact capture instructions.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_visual_evidence_report(path: Path = VISUAL_EVIDENCE_REPORT_PATH) -> Path:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    results = check_visual_evidence()
    path.write_text(visual_evidence_to_markdown(results), encoding="utf-8")
    return path


def main() -> None:
    report_path = write_visual_evidence_report()
    print(f"Wrote {report_path}")


if __name__ == "__main__":
    main()
