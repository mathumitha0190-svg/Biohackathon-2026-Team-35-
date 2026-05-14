# Judge Q&A

> This tool supports triage and investigation planning. It is not a diagnosis.

## Is this diagnosing PCOS?

No. The app reports PCOS triage risk, guideline evidence, missing exclusions, differential red flags, and a recommended next step. It is framed as investigation planning support for clinicians.

## Why logistic regression instead of a more complex model?

The MVP prioritizes interpretability, speed, and defensible coefficient-based explanations. Logistic regression fits the demo goal because judges can see top drivers and tier-level validation without requiring SHAP or a black-box model.

## What PCOS criteria does the app follow?

The checklist is aligned to adult PCOS evidence areas used in guideline-based assessment: ovulatory dysfunction, hyperandrogenism, ovarian morphology or AMH support, exclusion gaps, and metabolic risk. The cited rationale is in `docs/evidence_dossier.md`.

## How does the app handle AMH and ultrasound?

AMH and ultrasound features are used only in the full diagnostic model tier. They are not standalone answers. If age is adolescent-range, AMH or ultrasound evidence is flagged as inappropriate for adult-rule interpretation.

## Why include an endometriosis module?

PCOS and endometriosis can both appear in gynecologic triage, but the supplementary endometriosis dataset is synthetic and not merged into the classifier. The app uses intake-only pain red flags to recommend gynecology or endometriosis evaluation when the pain pattern is prominent.

## What are the dataset limitations?

The PCOS dataset has 541 labeled rows from a limited hospital context. It may not generalize across geography, ethnicity, care setting, or age distribution. The file is `without_infertility`, so infertility is not used as a PCOS model feature.

## How should judges interpret the validation metrics?

Metrics are suitable for hackathon evidence, not clinical deployment approval. The generated report includes AUROC, AUPRC, sensitivity, specificity, F1, Brier score, confidence intervals, calibration bins, thresholds, and subgroup caveats.

## What does subgroup analysis prove?

It proves that subgroup validity was considered transparently. It does not prove fairness or safety. Small groups or single-class groups are marked insufficient.

## What happens when labs or ultrasound are missing?

The app falls back to the most complete available tier. It does not crash, and it surfaces missing evidence so a clinician can decide what to collect next.

## What would be required before real deployment?

External prospective validation, local calibration, governance review, clinician usability testing, audit logging, and clinical sign-off. The current project is a judge-ready prototype, not a clinical device.

## What should be shown first if time is short?

Open `docs/judge_one_pager.md`, then run the app and show `Typical PCOS`, `Endometriosis-like`, and `4 Evidence`. Finish with `reports/preflight_submission_report.md` showing strict screenshot readiness.
