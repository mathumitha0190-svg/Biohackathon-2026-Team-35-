# PCOS Navigator: Evidence-Based Triage for Earlier Women's Health Diagnosis

## Winning Thesis

Build **PCOS Navigator**, a clinician-facing decision support prototype that helps primary care doctors and hackathon judges see the next right clinical action, not just a model score.

Position it as:

> An evidence-based triage and diagnostic pathway assistant that combines guideline-based reasoning, interpretable ML risk prediction, differential-diagnosis flags, and equity-aware deployment tiers to reduce missed PCOS cases.

Do **not** pitch this as "AI diagnoses PCOS." The safer and stronger claim is:

> PCOS Navigator supports earlier recognition, structured evidence review, and prioritization of follow-up tests or referral. It does not replace clinical diagnosis.

This framing directly matches the challenge: improve diagnostic accuracy for women's health, use the required PCOS dataset, address overlap with endometriosis, consider disparities, and produce a feasible clinical workflow.

## Why This Can Win

The project should win on **clinical validity plus implementation realism**. A basic classifier can show accuracy, but judges will likely reward the team that understands why PCOS is hard to diagnose in real life:

- PCOS has heterogeneous phenotypes: some patients have obesity or metabolic risk, others are lean; some have obvious hirsutism/acne, others need biochemical or ovarian evidence.
- PCOS diagnosis is not one lab test. The 2023 International Evidence-Based PCOS Guideline builds on Rotterdam-style criteria: two of clinical/biochemical hyperandrogenism, ovulatory dysfunction, and polycystic ovarian morphology by ultrasound or adult AMH, after excluding other causes.
- If irregular cycles and hyperandrogenism are both present in adults, ultrasound or AMH is not required for diagnosis.
- AMH should **not** be used as a standalone PCOS test and should not be used for adolescent diagnosis.
- WHO describes PCOS as affecting about 10-13% of reproductive-age women globally, with up to 70% undiagnosed.
- WHO describes endometriosis as a condition with severe menstrual pain, chronic pelvic pain, infertility, bloating/nausea, and common diagnosis delays, making it a good overlap and referral comparator.

The strongest story is:

> Missed PCOS is not mainly a missing-model problem. It is a pathway problem: clinicians need a structured way to synthesize symptoms, identify missing exclusions, recognize atypical phenotypes, and decide the next best step.

## Core Product

The tool should produce four outputs from one patient intake:

| Output | What it shows | Why judges care |
|---|---|---|
| PCOS risk tier | Low, medium, high risk with calibrated probability | Demonstrates diagnostic prediction |
| Guideline checklist | Evidence for ovulatory dysfunction, hyperandrogenism, ovarian morphology/AMH, and exclusion gaps | Demonstrates clinical validity |
| Differential flags | Endometriosis-like pain pattern, endocrine exclusion gaps, lean/atypical PCOS, metabolic risk | Demonstrates patient heterogeneity |
| Next-best action | Suggested test, referral, or monitoring step | Demonstrates workflow usefulness |

The demo should feel like a clinical pathway assistant, not a generic health tracker.

## Dataset Reality Check

Use these facts in the methodology section so the team sounds careful:

| Dataset | Role | Key constraint |
|---|---|---|
| `(Main_Dataset)_PCOS_data_without_infertility.xlsx` | Core supervised PCOS dataset | Actual labeled sheet has 541 usable rows: 177 PCOS-positive and 364 PCOS-negative. The workbook also contains blank/trailing rows that must be filtered. |
| `(Supplementary_Dataset)_structured_endometriosis_data.csv` | Differential red-flag/stress-test dataset | 10,000 synthetic rows with age, menstrual irregularity, chronic pain, hormone abnormality, infertility, BMI, and diagnosis. Do not merge directly into the PCOS classifier. |
| Single-cell files | Optional biological grounding | Too large and time-consuming for the main deliverable. Use only as a literature/mechanism visual if the core product is already complete. |

Important corrections to the current plan:

- The main PCOS file is named `without_infertility`; do not list infertility as a main PCOS model feature unless it is collected separately in the prototype intake.
- The PCOS sheet's `Cycle(R/I)` values appear as `2`, `4`, and one `5`, while the guide text is inconsistent. Treat this as a data dictionary issue and audit it before modeling.
- Drop identifiers: `Sl. No` and `Patient File No.`
- Do not use `Blood Group` as a predictive feature unless you have a strong clinical rationale. It is likely noise and can make the model look unserious.
- Treat `Pregnant(Y/N)`, beta-HCG, and pregnancy status as clinical branching/exclusion context, not ordinary risk-score drivers.
- Treat `Marriage Status (Yrs)` and `No. of abortions` as sensitive/social variables. Run models with and without them; prefer excluding them from the demo unless they clearly serve a clinically justified purpose.
- BMI, FSH/LH ratio, and waist:hip ratio are derived or partially derived features. Document whether you use raw components, derived variables, or both.

## Technical Plan

### Phase 1: Data Cleaning and Audit

Create a reproducible preprocessing notebook or script that:

1. Loads the second worksheet from the PCOS workbook.
2. Filters rows where `PCOS (Y/N)` is blank.
3. Standardizes column names into snake_case.
4. Converts binary columns to 0/1.
5. Audits `Cycle(R/I)` coding before recoding.
6. Recomputes BMI from height and weight and flags mismatches.
7. Recomputes FSH/LH ratio and waist:hip ratio and flags mismatches.
8. Checks impossible or suspicious values for height, weight, BMI, AMH, beta-HCG, FSH, LH, TSH, PRL, RBS, blood pressure, follicle counts, and endometrium thickness.
9. Splits data before imputation to avoid leakage.
10. Stores a preprocessing log with dropped columns, recodes, missing values, and outlier rules.

Deliverable: `data_profile.md` or notebook section with row counts, class balance, feature types, missingness, and preprocessing decisions.

### Phase 2: Resource-Tiered Models

Build three versions. This is one of the strongest parts of the project because it maps directly to feasibility and equity.

| Model tier | Features | Intended setting | Judge-facing value |
|---|---|---|---|
| History-only | Age, BMI or height/weight, cycle pattern, weight gain, hair growth, skin darkening, hair loss, pimples, lifestyle self-report if retained | Primary care, telehealth, low-resource triage | Shows accessibility without labs or ultrasound |
| Basic clinical | History-only plus BP, RBS/glucose, TSH, PRL, FSH, LH, hemoglobin, waist/hip | Clinic with basic tests | Shows practical implementation |
| Full diagnostic | Basic clinical plus AMH, follicle counts, follicle size, endometrium | Specialist setting | Shows maximum available performance |

Do not let the full model be the whole story. Full-model accuracy will be less impressive if it mainly learns features already used in clinical diagnosis. The winning comparison is the **incremental value curve**:

> How much performance do we gain as we move from history-only to basic clinic to full specialist data?

### Phase 3: Baselines and Final Model

Build these baselines:

| Model | Purpose |
|---|---|
| Regularized logistic regression | Transparent clinical baseline |
| Random forest or gradient boosting | Stronger nonlinear benchmark |
| Guideline rule engine | Non-ML clinical reference |
| Hybrid score | ML probability plus guideline checklist plus missing-test recommender |

Use the hybrid score in the demo:

```text
Final output = calibrated PCOS risk + guideline evidence checklist + exclusion gaps + next-best action
```

The model is not the product. The product is the pathway.

### Phase 4: Validation Strategy

Because the labeled PCOS dataset is small, the evaluation must look rigorous:

1. Use stratified train/validation/test splitting.
2. Use repeated stratified cross-validation on the training set.
3. Keep the final test set untouched until the end.
4. Report confidence intervals with bootstrap resampling.
5. Calibrate probabilities using Platt scaling or isotonic regression.
6. Pick a screening threshold that prioritizes sensitivity, then clearly report the specificity tradeoff.
7. Compare all three resource tiers using the same split.
8. Run ablations excluding sensitive/social variables.

Report these metrics:

| Metric | Why it matters |
|---|---|
| AUROC | Overall discrimination |
| AUPRC | Useful with class imbalance |
| Sensitivity/recall | Missed PCOS is the key harm |
| Specificity | Avoids unnecessary referral |
| F1-score | Balances positive-class performance |
| Brier score | Probability quality |
| Calibration curve | Whether risk scores mean what they say |
| Confusion matrix | Easy for judges to understand |
| Decision threshold table | Makes tradeoffs explicit |
| SHAP or coefficient plot | Explains drivers |

Set the threshold around the clinical purpose:

> For a triage tool, optimize for high sensitivity, then use the next-best-step layer to reduce unnecessary escalation.

### Phase 5: Clinical Rule Engine

Implement a simple rule engine that outputs evidence categories instead of pretending to make a final diagnosis.

| Criterion area | Evidence in this project |
|---|---|
| Ovulatory dysfunction | Irregular cycle coding, cycle length, menstrual history intake |
| Clinical hyperandrogenism | Hair growth, acne/pimples, hair loss; optionally clinician-entered hirsutism score |
| Biochemical hyperandrogenism | Not directly available in the PCOS dataset unless external androgen labs are collected in the app |
| Ovarian morphology / AMH | AMH and ultrasound follicle features in full model; thresholds should be configurable and documented |
| Exclusion gaps | TSH, PRL, FSH, pregnancy/beta-HCG context, and missing 17-OH progesterone or other indicated workup |
| Metabolic risk | BMI, waist:hip, BP, RBS/glucose, family history if added in intake |

Important clinical guardrails:

- Adult AMH may support PCOM evidence, but do not use AMH as a standalone diagnosis.
- Use either AMH or ultrasound evidence for PCOM where appropriate; do not imply that both are always required.
- If the intake is adolescent or early post-menarche, flag that adult ultrasound/AMH rules are not appropriate. If age at menarche is unavailable, state that the prototype is adult-focused.
- Rapid-onset or severe hyperandrogenism should trigger "consider non-PCOS causes" rather than a confident PCOS pathway.

## Differential Diagnosis Layer

Use the endometriosis dataset carefully:

> Because the endometriosis dataset is synthetic and has a different feature space, we use it as a differential-diagnosis stress test and symptom-overlap module, not as a direct combined PCOS/endometriosis classifier.

Add endometriosis-specific intake questions even if they are not in the PCOS dataset:

- Chronic pelvic pain level
- Severe menstrual pain
- Pain with intercourse
- Bowel or urinary pain around menstruation
- Heavy bleeding
- Bloating or nausea
- Infertility or difficulty conceiving

Use simple red-flag logic:

| Pattern | Output |
|---|---|
| Irregular cycles plus hyperandrogenism signs | PCOS pathway likely; check exclusions |
| Chronic pelvic pain plus severe menstrual pain or infertility | Endometriosis referral/workup flag |
| PCOS signs plus major pain symptoms | Possible overlap; broader gynecology evaluation |
| Weak PCOS evidence plus abnormal TSH/PRL/pregnancy context | Exclusion-first pathway |
| Strong PCOS signs with normal BMI | Lean PCOS alert; do not dismiss |
| Missing key evidence | Collect missing tests rather than overdiagnosing |

This will score better than forcing a scientifically weak all-in-one classifier.

## Prototype Plan

Build a small Streamlit or web dashboard with four screens.

### Screen 1: Patient Intake

Inputs:

- Age and adult/adolescent flag
- Height and weight
- Cycle regularity and cycle length
- Weight gain
- Hair growth
- Acne/pimples
- Hair loss
- Skin darkening
- Chronic pelvic pain level
- Severe menstrual pain
- Pain with intercourse
- Bowel/urinary pain around periods
- Heavy bleeding
- Bloating/nausea
- Difficulty conceiving, if relevant
- Optional labs: TSH, PRL, FSH, LH, AMH, RBS/glucose, hemoglobin, beta-HCG
- Optional ultrasound: follicle counts, ovarian morphology notes, endometrium thickness

### Screen 2: Risk Result

Example:

```text
PCOS triage risk: High
Probability: 0.82
Confidence: Moderate
Main drivers: irregular cycles, clinical hyperandrogenism signs, elevated AMH, increased follicle count
Important gaps: pregnancy status, 17-OH progesterone, androgen lab not available
```

### Screen 3: Guideline Checklist

Show a compact checklist:

| Evidence area | Status | Notes |
|---|---|---|
| Ovulatory dysfunction | Supported | Irregular cycles |
| Hyperandrogenism | Supported | Hair growth/acne/hair loss signs |
| PCOM / AMH | Available or missing | Do not require if first two criteria are present in adults |
| Exclusions | Incomplete | TSH/PRL/beta-HCG available; 17-OHP missing |
| Endometriosis red flags | Moderate or high | Pain pattern suggests referral |
| Metabolic risk | Present or absent | BMI, BP, RBS/glucose |

### Screen 4: Next Best Action

Examples:

| Situation | Recommendation |
|---|---|
| High PCOS risk, missing exclusions | Complete endocrine exclusion panel before confirming diagnosis |
| High PCOS risk, metabolic concern | Screen glycemic status, BP, lipids if available, and counsel lifestyle support |
| Endometriosis-like pain pattern | Consider gynecology referral and endometriosis evaluation |
| Low-resource setting | Use symptom-first triage, then prioritize the smallest useful lab set |
| Lean patient with strong PCOS signs | Do not dismiss due to normal BMI; continue guideline pathway |

Include a clear safety line in the UI:

> This tool supports triage and investigation planning. It is not a diagnosis and must be interpreted by a qualified clinician.

## Demo Cases To Prepare

Prepare four scripted patient cases for the live demo:

| Case | Purpose | Expected output |
|---|---|---|
| Typical PCOS | Obvious irregular cycles, hyperandrogenism, metabolic risk | High PCOS risk, metabolic screening |
| Lean PCOS | Normal BMI but irregular cycles and androgen signs | High/medium risk, lean PCOS warning |
| Endometriosis-like presentation | Severe pain, infertility, bloating, less androgen evidence | Endometriosis referral flag |
| Incomplete data | Irregular cycles but missing labs and weak androgen evidence | Missing-test recommender |

This prevents the presentation from depending on a random live input.

## Equity and Implementation Strategy

Make equity concrete rather than rhetorical:

| Equity issue | Product response |
|---|---|
| Low-resource settings may lack ultrasound or AMH | History-only and basic-clinic model tiers |
| Lean PCOS may be missed due to BMI stereotypes | Dedicated lean PCOS flag |
| Pain may be normalized or dismissed | Endometriosis red-flag checklist |
| Ethnic presentation may vary | Subgroup reporting where data allows; avoid one-size-fits-all thresholds |
| Sensitive variables may encode social bias | Exclude or ablate marriage/abortion variables and disclose decision |
| Model trained on Kerala hospital data may not generalize | State need for external validation before clinical deployment |

Add a "deployment maturity" statement:

> Hackathon prototype: retrospective dataset validation and simulated patient intake. Next step: prospective validation in primary care or gynecology clinics before real clinical use.

## Scoring Strategy By Rubric

| Rubric area | What to show |
|---|---|
| Clinical & Scientific Validity, 30% | 2023 guideline alignment, Rotterdam-style checklist, exclusion logic, phenotype-aware reasoning, PCOS biology, metabolic risk, endometriosis overlap |
| Diagnostic Accuracy, 20% | Tiered model comparison, sensitivity/specificity/AUROC/AUPRC, calibration, threshold table, confusion matrix |
| Feasibility & Implementation, 20% | History-only, basic-clinic, and full-specialist pathways; low-resource workflow; minimal required inputs |
| Innovation & Creativity, 12% | Next-best-test recommender, missing-evidence logic, differential red flags, lean/atypical phenotype support |
| Impact & Public Health Value, 10% | Earlier recognition, reduced missed cases, metabolic risk screening, referral prioritization, underserved settings |
| Methodology & Scientific Rigor, 10% | Split-before-imputation, cross-validation, calibration, bootstrap CIs, ablations, subgroup checks |
| Code Quality & Technical Execution, 5% | Clean repo, reproducible pipeline, saved model, README, requirements file, deterministic preprocessing |
| Presentation & Clarity, 3% | One strong clinical story, clean demo, four prepared patient cases, clear limitations |

## Best Project Title

Use this title:

> **PCOS Navigator: Evidence-Based Triage for Earlier Women's Health Diagnosis**

Backup options:

- **PCOS Pathway Assistant: Interpretable Decision Support for Earlier PCOS Detection**
- **From Symptoms to Next Step: Guideline-Based PCOS Triage**
- **Not "Just Stress": Reducing Missed PCOS Through Structured Diagnostic Triage**

## Final Presentation Structure

Use 8 slides:

1. **The problem**: PCOS is common, underdiagnosed, heterogeneous, and often delayed.
2. **Why diagnosis is hard**: No single test; overlapping symptoms; atypical and lean phenotypes; exclusion workup is often incomplete.
3. **Our solution**: PCOS Navigator gives risk score, guideline checklist, differential flags, and next-best action.
4. **Data**: Required PCOS dataset, synthetic endometriosis dataset for overlap flags, optional biological grounding.
5. **Methods**: Resource-tiered models, rule engine, preprocessing audit, calibration, threshold selection.
6. **Results**: Show tiered metrics, calibration, confusion matrix, SHAP/coefficient drivers, and threshold tradeoff.
7. **Demo**: Run two or three prepared patient cases, including lean PCOS and endometriosis-like pain.
8. **Impact and implementation**: Low-resource pathway, clinician workflow, equity safeguards, future prospective validation.

## Build Checklist

Minimum viable version:

- [ ] Clean PCOS workbook into one analysis-ready CSV.
- [ ] Write preprocessing audit.
- [ ] Train logistic regression baseline.
- [ ] Train one stronger tree/boosting model.
- [ ] Build guideline checklist rules.
- [ ] Add endometriosis red-flag module.
- [ ] Create dashboard intake and result pages.
- [ ] Prepare four demo cases.
- [ ] Write README with limitations and clinical safety statement.

Stretch goals:

- [ ] Add calibration curve and Brier score.
- [ ] Add bootstrap confidence intervals.
- [ ] Add subgroup checks by BMI group and age group.
- [ ] Add SHAP explanations.
- [ ] Add generated patient summary for clinician handoff.
- [ ] Add one PCOS biology figure if time allows.

## What To Avoid

- Do not build only a generic period tracker.
- Do not claim the model diagnoses PCOS or replaces doctors.
- Do not report accuracy alone.
- Do not ignore calibration.
- Do not merge PCOS and endometriosis datasets into one naive classifier.
- Do not overclaim from 541 labeled PCOS rows.
- Do not use single-cell analysis unless the core product is already working.
- Do not rely on AMH as a standalone diagnostic answer.
- Do not hide the dataset's limited geography and generalizability.
- Do not use sensitive/social variables without justification and ablation.

## References To Cite

- 2023 International Evidence-Based Guideline for PCOS, JCEM: https://academic.oup.com/jcem/article/108/10/2447/7242360
- WHO PCOS fact sheet: https://www.who.int/news-room/fact-sheets/detail/polycystic-ovary-syndrome
- WHO endometriosis fact sheet: https://www.who.int/news-room/fact-sheets/detail/endometriosis

## One-Sentence Closing

PCOS Navigator wins by making the model clinically useful: it predicts risk, explains the evidence, identifies what is missing, flags overlapping conditions, and recommends the next best step without pretending to replace clinical judgment.
