# Final Demo Rehearsal

> This tool supports triage and investigation planning. It is not a diagnosis.

Use this page as the last live-demo rehearsal before judging. The goal is to show the clinical pathway clearly, not to overclaim the model.

## 60-Second Judge Walkthrough

1. Start on `1 Intake` with `Typical PCOS` selected.
2. Point to the safety statement and say the app supports triage risk and investigation planning.
3. Show the top summary row: risk tier, probability, model tier, confidence, and recommended next step.
4. Open `2 Risk` and show the probability gauge plus coefficient contribution chart.
5. Open `3 Checklist` and show guideline evidence, exclusions, and adolescent caution if relevant.
6. Open `4 Evidence` and show validation metrics, calibration, thresholds, and subgroup caveats.
7. Open `5 Action` and show grouped actions plus clinician handoff summary.

## 5-Minute Live Demo Timing

| Time | Segment | What to show |
|---|---|---|
| 0:00-0:30 | Problem and safety | PCOS triage needs pathway support; this is not a diagnosis. |
| 0:30-1:30 | Typical PCOS | Complete guideline pathway, high triage risk, and next step. |
| 1:30-2:10 | Lean PCOS | Normal BMI does not dismiss cycle and androgen evidence. |
| 2:10-2:50 | Endometriosis-like | Differential red flags route toward gynecology review. |
| 2:50-3:30 | Incomplete Data | History-only fallback avoids crashing or overclaiming. |
| 3:30-4:30 | Model Evidence | Confidence intervals, calibration, selected threshold, and subgroup caveats. |
| 4:30-5:00 | Close | The app turns a model score into a clinician-facing triage pathway. |

## Screenshot Capture Checklist

Save these files under `assets/screenshots/` after running the app at `http://localhost:8501`.

| Filename | Case and tab | Purpose |
|---|---|---|
| `01_intake_summary.png` | `Typical PCOS`, `1 Intake` | Sidebar demo path, intake, and top summary row. |
| `02_risk_result.png` | `Typical PCOS`, `2 Risk` | Probability gauge and coefficient contribution chart. |
| `03_guideline_checklist.png` | `Typical PCOS`, `3 Checklist` | Guideline statuses and evidence table. |
| `04_model_evidence.png` | `Typical PCOS`, `4 Evidence` | Metrics, calibration, thresholds, and subgroup summary. |
| `05_next_action_handoff.png` | `Endometriosis-like`, `5 Action` | Differential flags and clinician handoff summary. |
| `06_readiness_export.png` | File explorer or report view | Readiness report or export folder contents. |

After screenshots are captured, run:

```powershell
uv run python scripts/check_visual_evidence.py
uv run python scripts/preflight_submission.py --strict-screenshots
uv run python scripts/export_presentation.py
```

## Closing Pitch

PCOS Navigator is a clinician-facing triage assistant. It combines resource-tiered risk prediction with guideline evidence, exclusion gaps, differential red flags, and recommended next steps. The value is not just the score; it is the structured handoff that helps a clinician decide what evidence is present, what is missing, and what should happen next.
