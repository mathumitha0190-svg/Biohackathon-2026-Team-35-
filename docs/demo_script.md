# PCOS Navigator Demo Script

## 5-Minute Run Of Show

### 0:00-0:30 - Problem

PCOS is common, heterogeneous, and often missed. The tool is not trying to diagnose PCOS. It helps clinicians structure triage: risk, guideline evidence, differential red flags, and the recommended next step.

Safety line to say out loud:

> This tool supports triage and investigation planning. It is not a diagnosis.

### 0:30-1:00 - Open The App

Run:

```powershell
uv run streamlit run app.py
```

Open:

```text
http://localhost:8501
```

Point out the tabs:

- Patient Intake
- Risk Result
- Guideline Checklist
- Model Evidence
- Next Action

### 1:00-2:00 - Case 1: Typical PCOS

Click the sidebar demo case:

```text
Typical PCOS
```

Click path:

1. `Patient Intake`: show irregular cycles, androgen signs, metabolic data, AMH/ultrasound fields.
2. `Risk Result`: show high triage risk, probability, confidence, and coefficient contribution chart.
3. `Guideline Checklist`: show ovulatory dysfunction, clinical hyperandrogenism, ovarian morphology/AMH, exclusions, and metabolic risk.
4. `Next Action`: show endocrine exclusions and metabolic screening.

Speaker point:

> The model score is not the endpoint. The useful output is the pathway: what evidence is present, what is missing, and what to do next.

### 2:00-2:50 - Case 2: Lean PCOS

Click:

```text
Lean PCOS
```

Click path:

1. `Risk Result`: show that normal BMI does not eliminate risk.
2. `Guideline Checklist`: show irregular cycles and androgen signs.
3. `Next Action`: highlight the lean PCOS alert.

Speaker point:

> This directly addresses a common clinical failure mode: dismissing PCOS because the patient is not overweight.

### 2:50-3:40 - Case 3: Endometriosis-Like

Click:

```text
Endometriosis-like
```

Click path:

1. `Patient Intake`: show pain features.
2. `Next Action`: show endometriosis-pattern red flags.
3. `Guideline Checklist`: show weaker PCOS evidence.

Speaker point:

> The system does not force all symptoms into PCOS. It flags when pain-pattern symptoms warrant broader gynecology evaluation.

### 3:40-4:20 - Case 4: Incomplete Data

Click:

```text
Incomplete Data
```

Click path:

1. `Risk Result`: show fallback to the history-only tier.
2. `Guideline Checklist`: show incomplete exclusions.
3. `Next Action`: show missing evidence and low-resource pathway.

Speaker point:

> The app degrades gracefully. If labs and ultrasound are missing, it still supports structured triage instead of failing or overclaiming.

### 4:20-5:00 - Model Evidence And Close

Click:

```text
Model Evidence
```

Show:

- tier comparison
- selected screening threshold
- calibration plot
- threshold tradeoff table
- subgroup summary

Closing line:

> PCOS Navigator wins by making the model clinically useful: it predicts triage risk, explains evidence, surfaces missing exclusions, flags overlapping conditions, and recommends the next step without replacing clinical judgment.
