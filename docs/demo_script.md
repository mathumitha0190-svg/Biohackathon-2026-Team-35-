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

- 1 Intake
- 2 Risk
- 3 Checklist
- 4 Evidence
- 5 Action

Point out the summary row:

- PCOS triage risk
- probability
- model tier
- confidence
- recommended next step

### 1:00-2:00 - Case 1: Typical PCOS

Click the sidebar demo case:

```text
Typical PCOS
```

Click path:

1. `1 Intake`: show irregular cycles, androgen signs, metabolic data, AMH/ultrasound fields.
2. Summary row: show high triage risk and recommended next step.
3. `2 Risk`: show probability, confidence, and coefficient contribution chart.
4. `3 Checklist`: show ovulatory dysfunction, clinical hyperandrogenism, ovarian morphology/AMH, exclusions, and metabolic risk.
5. `5 Action`: show grouped PCOS pathway, missing evidence, differential flags, and recommended next step.

Speaker point:

> The model score is not the endpoint. The useful output is the pathway: what evidence is present, what is missing, and what to do next.

### 2:00-2:50 - Case 2: Lean PCOS

Click:

```text
Lean PCOS
```

Click path:

1. `2 Risk`: show that normal BMI does not eliminate risk.
2. `3 Checklist`: show irregular cycles and androgen signs.
3. `5 Action`: highlight the lean PCOS alert.

Speaker point:

> This directly addresses a common clinical failure mode: dismissing PCOS because the patient is not overweight.

### 2:50-3:40 - Case 3: Endometriosis-Like

Click:

```text
Endometriosis-like
```

Click path:

1. `1 Intake`: show pain features.
2. `5 Action`: show endometriosis-pattern red flags.
3. `3 Checklist`: show weaker PCOS evidence.

Speaker point:

> The system does not force all symptoms into PCOS. It flags when pain-pattern symptoms warrant broader gynecology evaluation.

### 3:40-4:20 - Case 4: Incomplete Data

Click:

```text
Incomplete Data
```

Click path:

1. `2 Risk`: show fallback to the history-only tier.
2. `3 Checklist`: show incomplete exclusions.
3. `5 Action`: show missing evidence and low-resource pathway.

Speaker point:

> The app degrades gracefully. If labs and ultrasound are missing, it still supports structured triage instead of failing or overclaiming.

### 4:20-5:00 - Model Evidence And Close

Click:

```text
4 Evidence
```

Show:

- tier comparison
- selected screening threshold
- calibration plot
- threshold tradeoff table
- subgroup summary

Closing line:

> PCOS Navigator wins by making the model clinically useful: it predicts triage risk, explains evidence, surfaces missing exclusions, flags overlapping conditions, and recommends the next step without replacing clinical judgment.
