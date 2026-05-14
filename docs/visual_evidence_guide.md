# Visual Evidence Guide

Use this guide to capture a compact screenshot set for judges and slides. Screenshots are optional but recommended because they let judges verify the app, model evidence, and final readiness flow without reading code.

## Capture Setup

- Browser size: 1440 x 1000 or larger.
- App URL: `http://localhost:8501`
- Start command: `uv run streamlit run app.py`
- Recommended browser zoom: 90-100%.
- Store files in: `assets/screenshots/`
- Use PNG format and exact filenames below.

## Required Screenshot Set

| Filename | Demo case / view | What to capture | Rubric proof |
|---|---|---|---|
| `01_intake_summary.png` | `Typical PCOS`, `1 Intake` | Sidebar demo path, why-case text, intake inputs, and top summary row | Feasibility, presentation clarity |
| `02_risk_result.png` | `Typical PCOS`, `2 Risk` | Triage risk, probability gauge, confidence, and coefficient contribution chart | Diagnostic accuracy, interpretability |
| `03_guideline_checklist.png` | `Typical PCOS`, `3 Checklist` | Checklist table and status badges | Clinical and scientific validity |
| `04_model_evidence.png` | `Typical PCOS`, `4 Evidence` | Tier metrics, selected threshold, calibration plot, threshold table, subgroup summary | Methodology, validation rigor |
| `05_next_action_handoff.png` | `Endometriosis-like` or `Incomplete Data`, `5 Action` | Grouped actions, differential flags, missing evidence, handoff summary | Innovation, clinical workflow value |
| `06_readiness_export.png` | File explorer or rendered report | `reports/readiness_report.md` or `exports/pcos_navigator_presentation/` contents | Code quality, reproducibility, presentation readiness |

## Recommended Capture Order

1. Run `uv run python scripts/profile_data.py`.
2. Run `uv run python scripts/train_models.py`.
3. Run `uv run python scripts/check_readiness.py`.
4. Run `uv run python scripts/export_presentation.py`.
5. Run `uv run streamlit run app.py`.
6. Capture screenshots in the filename order above.
7. Run `uv run python scripts/check_visual_evidence.py`.

## Slide Usage

- Use `01_intake_summary.png` on the solution or demo slide.
- Use `02_risk_result.png` and `03_guideline_checklist.png` together to show model plus clinical reasoning.
- Use `04_model_evidence.png` on the methodology/results slide.
- Use `05_next_action_handoff.png` on the impact/implementation slide.
- Use `06_readiness_export.png` as backup evidence for reproducibility and code quality.

## Safety Reminder

Every screenshot used in slides should preserve or be accompanied by this statement:

> This tool supports triage and investigation planning. It is not a diagnosis.
