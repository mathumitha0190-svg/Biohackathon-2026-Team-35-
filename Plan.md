## <a id="_raqev23icv5h"></a>__Winning project idea__

Build __PCOS Pathway Assistant__: a clinician\-facing diagnostic support tool that helps primary care doctors identify PCOS earlier, distinguish it from endometriosis\-like presentations, and decide the next best investigation\.

Do __not__ pitch it as “AI diagnoses PCOS\.” Pitch it as:

“An evidence\-based triage and diagnostic pathway assistant that reduces missed PCOS cases by combining guideline\-based reasoning, interpretable ML risk prediction, differential\-diagnosis flags, and an equity\-aware implementation plan\.”

That directly matches the challenge: improve diagnostic accuracy for women’s health, use the provided PCOS dataset, consider overlapping conditions, disparities, implementation, and patient outcomes\.

## <a id="_h76qqwpbnizh"></a>__Why this is high\-scoring__

The current 2023 international PCOS guideline says adult PCOS diagnosis uses updated Rotterdam criteria: two of hyperandrogenism, ovulatory dysfunction, and polycystic ovaries on ultrasound or elevated AMH, after excluding other causes; if irregular cycles and hyperandrogenism are both present, ultrasound or AMH is not required\. WHO also describes PCOS as a major public\-health issue affecting an estimated 10–13% of women globally, with up to 70% undiagnosed\. Endometriosis is a good differential\-diagnosis comparator because WHO lists overlapping features such as severe menstrual pain, chronic pelvic pain, infertility, bloating, and diagnosis delays\.

So your solution should not just be “train model, show accuracy\.” That is too basic\.

Your angle should be:

PCOS is not one disease presentation\. It has phenotypes\. A good diagnostic system must detect typical PCOS, lean/atypical PCOS, and “could be PCOS but also investigate endometriosis/thyroid/prolactin/pregnancy causes\.”

## <a id="_2648whwd2h0x"></a>__Product design__

### <a id="_mo8x9hc8w0i"></a>__1\. Three\-level diagnostic assistant__

The tool gives doctors four outputs:

__A\. PCOS risk score  
__ A calibrated probability: low, medium, high risk\.

__B\. Guideline reasoning checklist  
__ Shows which Rotterdam\-style criteria are supported:

__Criterion__

__Evidence from patient data__

Ovulatory dysfunction

irregular cycle, cycle length

Hyperandrogenism proxy

hair growth, acne/pimples, hair loss, possibly hormone indicators

Polycystic ovarian morphology / AMH

follicle count, AMH, ultrasound\-related features

Exclusion prompts

TSH, PRL, beta\-HCG, pregnancy\-related checks

__C\. Differential\-diagnosis flags  
__ Flags cases where PCOS may not be the full story:

__Pattern__

__Suggested action__

High pelvic/chronic pain \+ infertility

consider endometriosis referral/workup

Abnormal TSH/PRL/pregnancy markers

exclude thyroid, prolactin, pregnancy\-related causes

Irregular cycles but weak androgen/ovarian evidence

collect missing tests instead of overdiagnosing

Strong PCOS signs but normal BMI

do not dismiss lean PCOS

__D\. Next\-best\-step recommendation  
__ Instead of only saying “PCOS likely,” the system says:

__Situation__

__Next step__

High risk, incomplete labs

order AMH / androgen / thyroid / prolactin panel

High risk, metabolic concern

screen glucose risk, BP, BMI, lifestyle risk

Endometriosis\-like symptoms

refer for gynecology evaluation

Low\-resource setting

use symptom\-first triage before expensive imaging

This is stronger than a normal ML classifier because it supports real clinical workflow\.

## <a id="_nwev1zgx0tqg"></a>__Technical plan__

### <a id="_8et3dp4j3a6p"></a>__Phase 1: Data cleaning__

Use the required PCOS clinical dataset as the core dataset\. The guide says it includes physical and clinical parameters such as age, BMI, menstrual cycle features, pregnancy history, FSH/LH, AMH, TSH, prolactin, vitamin D, glucose, symptoms, blood pressure, follicle counts, and endometrium thickness\.

Clean it carefully:

1. Drop identifiers: Sl\. No, Patient File No\.
2. Standardise column names\.
3. Convert Yes/No columns to 1/0\.
4. Recompute BMI from kg and height in meters to check for errors\.
5. Check impossible values: height, weight, AMH, beta\-HCG, follicle count, BP\.
6. Impute missing values using median/mode\.
7. Keep a preprocessing log so judges see reproducibility\.

Very important: make __three model versions__:

__Model__

__Features used__

__Why judges like it__

History\-only model

age, BMI, cycle, symptoms, infertility, weight gain

feasible in primary care / low\-resource settings

Basic clinical model

history \+ BP \+ glucose \+ FSH/LH \+ TSH \+ PRL

practical clinic setting

Full diagnostic model

all above \+ AMH \+ ultrasound follicle data

specialist/high\-accuracy setting

This is a big scoring move because it directly addresses feasibility, accessibility, and real\-world implementation\.

### <a id="_ixq2g0qmfj1y"></a>__Phase 2: Model building__

Build at least three baselines:

1. __Logistic Regression  
__ Simple, interpretable clinical baseline\.
2. __Random Forest or XGBoost/LightGBM  
__ Higher diagnostic performance\.
3. __Guideline\-based rule engine  
__ Not ML\. Uses Rotterdam\-style logic and missing\-data prompts\.

Then combine them:

Final output = ML probability \+ guideline checklist \+ missing\-test recommender\.

Metrics to report:

__Metric__

__Why__

AUROC

overall discrimination

Sensitivity/Recall

important because missing PCOS is harmful

Specificity

avoid over\-referral

F1\-score

class balance

Calibration curve

proves probabilities are meaningful

Confusion matrix

easy for judges to understand

SHAP feature importance

interpretability

For a diagnostic screening tool, choose a threshold that prioritises __high sensitivity__, because the goal is not to make a final diagnosis but to reduce missed cases\.

### <a id="_o0pxjvg5vjss"></a>__Phase 3: Differential diagnosis layer__

Use the endometriosis dataset carefully\. The guide says it is synthetic but realistic, with features like age, menstrual irregularity, chronic pain level, hormone abnormality, infertility, BMI, and diagnosis\.

Do __not__ pretend you can directly merge it perfectly with the PCOS dataset\. That would be scientifically weak\.

Instead, say:

“Because the endometriosis dataset is synthetic and has a different feature space, we use it as a differential\-diagnosis stress test and symptom\-overlap module rather than as a direct combined classifier\.”

Create simple flags:

__Symptom pattern__

__Output__

Irregular periods \+ hyperandrogenism signs

PCOS pathway

Chronic pelvic pain \+ infertility \+ severe menstrual pain

endometriosis pathway

Both PCOS signs and pain signs

possible overlap; recommend broader gynecology evaluation

Incomplete evidence

collect missing data

This will score better under __clinical validity__ than forcing a fake all\-in\-one classifier\.

## <a id="_fem1mody0v3t"></a>__Prototype plan__

Build a simple web app or notebook dashboard with 4 screens:

### <a id="_ph26jgf8tsnc"></a>__Screen 1: Patient intake__

Inputs:

- Age
- Weight / height
- Cycle regularity
- Cycle length
- Weight gain
- Hair growth
- Acne/pimples
- Hair loss
- Skin darkening
- Infertility
- Chronic pain level
- Exercise / fast food
- Optional labs and ultrasound values

### <a id="_kf3m6fixslj1"></a>__Screen 2: Risk result__

Example output:

PCOS risk: High  
 Confidence: Moderate  
 Key drivers: irregular cycle, high AMH, increased follicle count, hirsutism, weight gain  
 Missing exclusions: thyroid/prolactin/pregnancy checks incomplete

### <a id="_13gbf0p0ubeu"></a>__Screen 3: Guideline checklist__

Visual checklist:

- Ovulatory dysfunction: likely
- Hyperandrogenism: likely
- Ovarian morphology / AMH: available or missing
- Exclusion checks: incomplete
- Endometriosis red flags: moderate

### <a id="_zdgnbveghnl"></a>__Screen 4: Next action__

Example:

Recommended next step: complete endocrine exclusion panel, screen metabolic risk, and consider gynecology referral if chronic pelvic pain persists\.

This makes the demo feel clinically useful, not just technical\.

## <a id="_ldrq7cvy2pz9"></a>__Scoring strategy by rubric__

__Rubric area__

__What you should show__

Clinical & Scientific Validity, 30%

Align with 2023 PCOS guideline, explain Rotterdam criteria, PCOS biology, hormone/metabolic/ovarian mechanisms, exclusion of overlapping causes

Diagnostic Accuracy, 20%

Compare models, show sensitivity/specificity/AUROC, use high\-sensitivity threshold, show endometriosis overlap flags

Feasibility, 20%

Three deployment modes: primary\-care symptom screen, clinic lab model, specialist full model

Innovation, 12%

“Next\-best\-test” recommender \+ diagnostic delay risk \+ phenotype\-aware PCOS triage

Impact, 10%

Earlier identification, less dismissal, lower infertility/metabolic complication risk, low\-resource screening

Methodology, 10%

Proper train/test split, cross\-validation, calibration, SHAP, subgroup analysis

Code Quality, 5%

Clean repo, README, reproducible pipeline, requirements file, saved model

Presentation, 3%

Clear story, simple demo, strong visuals

The challenge’s judging criteria heavily reward clinical validity, diagnostic accuracy, feasibility, innovation, impact, methodology, code quality, and presentation clarity, so your submission should explicitly map every feature to those categories\.

## <a id="_4wezd7yeru25"></a>__The strongest project title__

Use one of these:

__Best professional title:  
__ __PCOS Pathway Assistant: An Interpretable Clinical Decision Support Tool for Earlier PCOS Detection and Differential Triage__

__More memorable title:  
__ __Not “Just Stress”: Reducing Missed PCOS Diagnoses with Evidence\-Based Diagnostic Triage__

__Most hackathon\-friendly:  
__ __PCOS Navigator: From Symptoms to Next Best Clinical Action__

I would choose:  
 __PCOS Navigator: Evidence\-Based Triage for Earlier Women’s Health Diagnosis__

## <a id="_6oh8cygkiaga"></a>__Final presentation structure__

Use 8 slides\.

1. __The problem  
__ Women with PCOS are often undiagnosed or delayed; PCOS is heterogeneous and overlaps with other conditions\.
2. __Why PCOS is hard to diagnose  
__ No single test, multiple phenotypes, overlapping symptoms, bias/dismissal\.
3. __Our solution  
__ PCOS Navigator: risk score \+ guideline checklist \+ differential flags \+ next\-best\-step\.
4. __Data used  
__ Required PCOS dataset, supplementary endometriosis dataset, optional single\-cell/literature grounding\.
5. __Methodology  
__ Three model tiers: history\-only, basic clinical, full diagnostic\. Include preprocessing, validation, explainability\.
6. __Results  
__ Show AUROC, sensitivity, specificity, confusion matrix, SHAP features, calibration\.
7. __Demo  
__ Enter a patient profile\. Show PCOS risk, evidence checklist, missing tests, endometriosis warning\.
8. __Impact and implementation  
__ Primary care, telehealth, low\-resource settings, patient summary, equitable triage, future validation\.

## <a id="_zcdhhjczcbir"></a>__What to avoid__

Do not build only a generic period tracker\.  
 Do not claim your model replaces doctors\.  
 Do not use accuracy alone\.  
 Do not ignore endometriosis\.  
 Do not merge PCOS and endometriosis datasets blindly\.  
 Do not overclaim if the dataset is small or synthetic\.  
 Do not spend too much time on single\-cell analysis unless your main product is already working\.

The winning direction is: __clinically grounded, interpretable, feasible, and demo\-able\.__

