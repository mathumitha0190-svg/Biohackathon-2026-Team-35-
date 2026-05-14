# Screenshot Assets

Place optional judge-facing screenshots in this folder.

Screenshot image files are ignored by git to keep the repository light. Use the exact filenames from `docs/visual_evidence_guide.md`:

- `01_intake_summary.png`
- `02_risk_result.png`
- `03_guideline_checklist.png`
- `04_model_evidence.png`
- `05_next_action_handoff.png`
- `06_readiness_export.png`

Run this check after capturing screenshots:

```powershell
uv run python scripts/check_visual_evidence.py
```
