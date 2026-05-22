# PCOS Navigator Visual Evidence Report

> This tool supports triage and investigation planning. It is not a diagnosis.

Screenshots are optional but recommended for judges and slides. Missing screenshots are warnings, not failures.

## Screenshot Checks

| Screenshot | Status | Rubric purpose | What it proves | Detail |
|---|---|---|---|---|
| `01_intake_summary.png` | WARN | Feasibility, presentation clarity | Shows sidebar demo path, why-case text, intake, and top summary row. | missing; capture and save to `C:\Users\angwm\source\Biohackathon-2026-Team-35-\assets\screenshots\01_intake_summary.png` |
| `02_risk_result.png` | WARN | Diagnostic accuracy, interpretability | Shows triage risk, probability gauge, confidence, and coefficient drivers. | missing; capture and save to `C:\Users\angwm\source\Biohackathon-2026-Team-35-\assets\screenshots\02_risk_result.png` |
| `03_guideline_checklist.png` | WARN | Clinical and scientific validity | Shows guideline checklist statuses and evidence table. | missing; capture and save to `C:\Users\angwm\source\Biohackathon-2026-Team-35-\assets\screenshots\03_guideline_checklist.png` |
| `04_model_evidence.png` | WARN | Methodology, validation rigor | Shows model metrics, calibration, threshold tradeoff, and subgroup summary. | missing; capture and save to `C:\Users\angwm\source\Biohackathon-2026-Team-35-\assets\screenshots\04_model_evidence.png` |
| `05_next_action_handoff.png` | WARN | Innovation, clinical workflow value | Shows grouped actions, differential flags, missing evidence, and handoff summary. | missing; capture and save to `C:\Users\angwm\source\Biohackathon-2026-Team-35-\assets\screenshots\05_next_action_handoff.png` |
| `06_readiness_export.png` | WARN | Code quality, reproducibility, presentation readiness | Shows readiness report or export bundle contents. | missing; capture and save to `C:\Users\angwm\source\Biohackathon-2026-Team-35-\assets\screenshots\06_readiness_export.png` |

## Capture Command Flow

```powershell
uv run python scripts/profile_data.py
uv run python scripts/train_models.py
uv run python scripts/check_readiness.py
uv run python scripts/export_presentation.py
uv run streamlit run app.py
```

See `docs/visual_evidence_guide.md` for exact capture instructions.
