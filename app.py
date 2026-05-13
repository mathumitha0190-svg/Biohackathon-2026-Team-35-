from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from pcos_navigator.clinical import assess_patient, clinician_handoff_summary
from pcos_navigator.config import MODEL_ARTIFACT_PATH, SAFETY_STATEMENT
from pcos_navigator.data import available_model_tier, load_clean_pcos
from pcos_navigator.demo_cases import DEMO_CASES
from pcos_navigator.modeling import load_artifact, predict_patient, save_artifacts, train_models


CASE_EXPLANATIONS = {
    "Typical PCOS": "Shows the complete pathway: high triage risk, guideline evidence, metabolic risk, and next-step planning.",
    "Lean PCOS": "Shows why normal BMI should not dismiss PCOS when cycle and androgen evidence are present.",
    "Endometriosis-like": "Shows differential triage when pain-pattern red flags are stronger than PCOS evidence.",
    "Incomplete Data": "Shows low-resource fallback when labs and ultrasound are missing.",
}

DEMO_PATH = [
    ("Typical PCOS", "complete pathway"),
    ("Lean PCOS", "normal-BMI PCOS handling"),
    ("Endometriosis-like", "differential red flags"),
    ("Incomplete Data", "history-only fallback"),
]


st.set_page_config(
    page_title="PCOS Navigator",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_resource(show_spinner=False)
def get_artifact() -> dict:
    if MODEL_ARTIFACT_PATH.exists():
        artifact = load_artifact()
        first_tier = next(iter(artifact.get("metrics", {}).get("tiers", {}).values()), {})
        if "confidence_intervals" in first_tier and "calibration_bins" in first_tier:
            return artifact
    df = load_clean_pcos()
    artifact, metrics = train_models(df)
    save_artifacts(artifact, metrics)
    return artifact


def yes_no(label: str, value: int | None = 0) -> int:
    options = {"No": 0, "Yes": 1}
    default = "Yes" if value == 1 else "No"
    return options[st.radio(label, options.keys(), index=list(options).index(default), horizontal=True)]


def optional_number(label: str, value: float | int | None, min_value: float = 0.0, step: float = 0.1) -> float | None:
    enabled = st.checkbox(f"Include {label}", value=value is not None)
    if not enabled:
        return None
    return st.number_input(label, min_value=min_value, value=float(value or min_value), step=step)


def default_case_values(case_name: str) -> dict:
    return DEMO_CASES.get(case_name, DEMO_CASES["Typical PCOS"]).copy()


def top_summary(prediction, assessment) -> dict[str, str]:
    next_step = assessment.next_actions[0] if assessment.next_actions else "Collect missing clinical evidence."
    return {
        "risk_tier": prediction.risk_tier,
        "probability": f"{prediction.probability:.0%}",
        "model_tier": prediction.tier,
        "confidence": assessment.confidence,
        "recommended_next_step": next_step,
    }


def grouped_actions(assessment) -> dict[str, list[str]]:
    groups = {
        "PCOS pathway": [],
        "Differential flags": [],
        "Missing evidence": [],
        "Recommended next step": [],
    }

    for action in assessment.next_actions:
        lower = action.lower()
        if "endometriosis" in lower or "gynecology" in lower:
            groups["Differential flags"].append(action)
        elif "missing" in lower or "exclusion" in lower or "collect" in lower or "low-resource" in lower:
            groups["Missing evidence"].append(action)
        elif "metabolic" in lower or "guideline" in lower or "lean pcos" in lower or "pcos" in lower:
            groups["PCOS pathway"].append(action)
        else:
            groups["Recommended next step"].append(action)

    if not groups["Differential flags"]:
        groups["Differential flags"].append("No endometriosis-pattern red flags from the provided intake.")
    for flag in assessment.differential_flags:
        if flag not in groups["Differential flags"]:
            groups["Differential flags"].append(flag)

    for item in assessment.checklist:
        if item.status in {"Missing", "Incomplete", "Caution"}:
            groups["Missing evidence"].append(f"{item.name}: {item.notes}")

    if assessment.next_actions:
        groups["Recommended next step"].append(assessment.next_actions[0])

    return groups


def patient_form(defaults: dict) -> dict:
    st.subheader("Patient Intake")
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        age = st.number_input("Age", min_value=12, max_value=55, value=int(defaults.get("age", 27)))
        height = st.number_input("Height (cm)", min_value=120.0, max_value=220.0, value=float(defaults.get("height_cm", 162)), step=0.5)
        weight = st.number_input("Weight (kg)", min_value=30.0, max_value=180.0, value=float(defaults.get("weight_kg", 70)), step=0.5)
        bmi_default = float(defaults.get("bmi") or (weight / ((height / 100) ** 2)))
        bmi = st.number_input("BMI", min_value=10.0, max_value=60.0, value=round(bmi_default, 1), step=0.1)
    with col_b:
        cycle_choice = st.radio(
            "Cycle pattern",
            ["Regular", "Irregular"],
            index=1 if defaults.get("cycle", 0) == 1 else 0,
            horizontal=True,
        )
        cycle = 1 if cycle_choice == "Irregular" else 0
        cycle_length = st.number_input("Cycle length (days)", min_value=10, max_value=120, value=int(defaults.get("cycle_length", 35)))
        weight_gain = yes_no("Weight gain", defaults.get("weight_gain", 0))
        hair_growth = yes_no("Hair growth / hirsutism", defaults.get("hair_growth", 0))
    with col_c:
        skin_darkening = yes_no("Skin darkening", defaults.get("skin_darkening", 0))
        hair_loss = yes_no("Hair loss", defaults.get("hair_loss", 0))
        pimples = yes_no("Acne / pimples", defaults.get("pimples", 0))
        pregnant = yes_no("Currently pregnant", defaults.get("pregnant", 0)) if st.checkbox("Include pregnancy status", value=defaults.get("pregnant") is not None) else None

    st.subheader("Optional Clinic Data")
    lab_a, lab_b, lab_c = st.columns(3)
    with lab_a:
        bp_systolic = optional_number("BP systolic", defaults.get("bp_systolic"), min_value=70, step=1)
        bp_diastolic = optional_number("BP diastolic", defaults.get("bp_diastolic"), min_value=40, step=1)
        rbs = optional_number("RBS / glucose", defaults.get("rbs"), min_value=40, step=1)
        hemoglobin = optional_number("Hemoglobin", defaults.get("hemoglobin"), min_value=4, step=0.1)
    with lab_b:
        tsh = optional_number("TSH", defaults.get("tsh"), min_value=0, step=0.1)
        prl = optional_number("PRL", defaults.get("prl"), min_value=0, step=0.1)
        fsh = optional_number("FSH", defaults.get("fsh"), min_value=0, step=0.1)
        lh = optional_number("LH", defaults.get("lh"), min_value=0, step=0.1)
    with lab_c:
        waist = optional_number("Waist (inch)", defaults.get("waist"), min_value=15, step=0.5)
        hip = optional_number("Hip (inch)", defaults.get("hip"), min_value=15, step=0.5)
        waist_hip_ratio = None if waist is None or hip in (None, 0) else waist / hip
        i_beta_hcg = optional_number("beta-HCG", defaults.get("i_beta_hcg"), min_value=0, step=0.1)

    st.subheader("Optional Ultrasound / AMH")
    us_a, us_b, us_c = st.columns(3)
    with us_a:
        amh = optional_number("AMH", defaults.get("amh"), min_value=0, step=0.1)
        endometrium = optional_number("Endometrium (mm)", defaults.get("endometrium"), min_value=0, step=0.1)
    with us_b:
        follicle_no_l = optional_number("Follicle count left", defaults.get("follicle_no_l"), min_value=0, step=1)
        follicle_no_r = optional_number("Follicle count right", defaults.get("follicle_no_r"), min_value=0, step=1)
    with us_c:
        avg_f_size_l = optional_number("Avg follicle size left", defaults.get("avg_f_size_l"), min_value=0, step=0.5)
        avg_f_size_r = optional_number("Avg follicle size right", defaults.get("avg_f_size_r"), min_value=0, step=0.5)

    st.subheader("Pain and Endometriosis Red Flags")
    pain_a, pain_b, pain_c = st.columns(3)
    with pain_a:
        chronic_pelvic_pain = st.slider("Chronic pelvic pain", 0, 10, int(defaults.get("chronic_pelvic_pain", 0)))
        severe_menstrual_pain = yes_no("Severe menstrual pain", defaults.get("severe_menstrual_pain", 0))
        pain_with_intercourse = yes_no("Pain with intercourse", defaults.get("pain_with_intercourse", 0))
    with pain_b:
        bowel_urinary_pain = yes_no("Bowel/urinary pain around periods", defaults.get("bowel_urinary_pain", 0))
        heavy_bleeding = yes_no("Heavy bleeding", defaults.get("heavy_bleeding", 0))
        bloating_nausea = yes_no("Bloating or nausea", defaults.get("bloating_nausea", 0))
    with pain_c:
        difficulty_conceiving = yes_no("Difficulty conceiving", defaults.get("difficulty_conceiving", 0))

    return {
        "age": age,
        "height_cm": height,
        "weight_kg": weight,
        "bmi": bmi,
        "cycle": cycle,
        "cycle_length": cycle_length,
        "weight_gain": weight_gain,
        "hair_growth": hair_growth,
        "skin_darkening": skin_darkening,
        "hair_loss": hair_loss,
        "pimples": pimples,
        "pregnant": pregnant,
        "bp_systolic": bp_systolic,
        "bp_diastolic": bp_diastolic,
        "rbs": rbs,
        "hemoglobin": hemoglobin,
        "tsh": tsh,
        "prl": prl,
        "fsh": fsh,
        "lh": lh,
        "waist": waist,
        "hip": hip,
        "waist_hip_ratio": waist_hip_ratio,
        "i_beta_hcg": i_beta_hcg,
        "amh": amh,
        "follicle_no_l": follicle_no_l,
        "follicle_no_r": follicle_no_r,
        "avg_f_size_l": avg_f_size_l,
        "avg_f_size_r": avg_f_size_r,
        "endometrium": endometrium,
        "chronic_pelvic_pain": chronic_pelvic_pain,
        "severe_menstrual_pain": severe_menstrual_pain,
        "pain_with_intercourse": pain_with_intercourse,
        "bowel_urinary_pain": bowel_urinary_pain,
        "heavy_bleeding": heavy_bleeding,
        "bloating_nausea": bloating_nausea,
        "difficulty_conceiving": difficulty_conceiving,
    }


def probability_chart(probability: float) -> go.Figure:
    return go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=probability * 100,
            number={"suffix": "%"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#2563eb"},
                "steps": [
                    {"range": [0, 35], "color": "#dcfce7"},
                    {"range": [35, 65], "color": "#fef3c7"},
                    {"range": [65, 100], "color": "#fee2e2"},
                ],
            },
        )
    )


def driver_chart(drivers: list[tuple[str, float]]) -> go.Figure:
    frame = pd.DataFrame(drivers, columns=["Feature", "Contribution"]).sort_values("Contribution")
    colors = ["#dc2626" if value > 0 else "#2563eb" for value in frame["Contribution"]]
    figure = go.Figure(
        go.Bar(
            x=frame["Contribution"],
            y=frame["Feature"],
            orientation="h",
            marker_color=colors,
        )
    )
    figure.update_layout(
        xaxis_title="Coefficient contribution",
        yaxis_title="",
        height=320,
        margin={"l": 120, "r": 20, "t": 20, "b": 40},
    )
    return figure


def calibration_chart(calibration_bins: list[dict]) -> go.Figure:
    frame = pd.DataFrame(calibration_bins)
    figure = go.Figure()
    figure.add_trace(
        go.Scatter(
            x=[0, 1],
            y=[0, 1],
            mode="lines",
            name="Perfect calibration",
            line={"dash": "dash", "color": "#64748b"},
        )
    )
    figure.add_trace(
        go.Scatter(
            x=frame["mean_predicted"],
            y=frame["observed_rate"],
            mode="lines+markers",
            name="Observed",
            marker={"size": frame["n"].clip(lower=6, upper=22)},
            line={"color": "#2563eb"},
        )
    )
    figure.update_layout(
        xaxis_title="Mean predicted probability",
        yaxis_title="Observed PCOS rate",
        xaxis={"range": [0, 1]},
        yaxis={"range": [0, 1]},
        height=360,
        margin={"l": 40, "r": 20, "t": 20, "b": 40},
    )
    return figure


def metric_ci_text(metric: str, tier_metrics: dict) -> str:
    ci = tier_metrics["confidence_intervals"].get(metric)
    if not ci:
        return f"{tier_metrics[metric]:.3f}"
    return f"{tier_metrics[metric]:.3f} ({ci['low']:.3f}-{ci['high']:.3f})"


def render_model_evidence(artifact: dict, active_tier: str) -> None:
    st.subheader("Model Evidence")
    st.caption("Shows the validation evidence judges can use to trust the triage score.")
    st.caption(SAFETY_STATEMENT)
    metrics = artifact["metrics"]["tiers"]
    tiers = list(metrics.keys())
    selected_tier = st.selectbox(
        "Evidence tier",
        tiers,
        index=tiers.index(active_tier) if active_tier in tiers else 0,
    )
    tier_metrics = metrics[selected_tier]

    comparison_rows = []
    for tier, values in metrics.items():
        selected = values["selected_threshold"]
        comparison_rows.append(
            {
                "Tier": tier,
                "AUROC (95% CI)": metric_ci_text("auroc", values),
                "AUPRC (95% CI)": metric_ci_text("auprc", values),
                "Sensitivity (95% CI)": metric_ci_text("sensitivity", values),
                "Specificity (95% CI)": metric_ci_text("specificity", values),
                "Brier (95% CI)": metric_ci_text("brier_score", values),
                "Screening threshold": f"{selected['threshold']:.2f}",
            }
        )
    st.dataframe(pd.DataFrame(comparison_rows), use_container_width=True, hide_index=True)

    threshold = tier_metrics["selected_threshold"]
    st.info(
        f"Selected screening threshold for {selected_tier}: {threshold['threshold']:.2f}. "
        f"Sensitivity {threshold['sensitivity']:.0%}, specificity {threshold['specificity']:.0%}; "
        f"{threshold['reason']}."
    )

    evidence_a, evidence_b = st.columns(2)
    with evidence_a:
        st.write("Calibration")
        st.plotly_chart(calibration_chart(tier_metrics["calibration_bins"]), use_container_width=True)
    with evidence_b:
        st.write("Threshold tradeoff")
        threshold_df = pd.DataFrame(tier_metrics["threshold_table"])
        st.dataframe(
            threshold_df[["threshold", "sensitivity", "specificity", "f1", "tp", "fp", "fn", "tn"]],
            use_container_width=True,
            hide_index=True,
        )

    subgroup_rows = []
    for group_name, group_metrics in tier_metrics["subgroup_metrics"].items():
        for segment, values in group_metrics.items():
            subgroup_rows.append(
                {
                    "Group": group_name,
                    "Segment": segment,
                    "n": values["n"],
                    "Positive": values["positive_count"],
                    "Status": values.get("reason", "ok"),
                    "AUROC": values.get("auroc"),
                    "Sensitivity": values.get("sensitivity"),
                    "Specificity": values.get("specificity"),
                }
            )
    st.write("Subgroup summary")
    st.dataframe(pd.DataFrame(subgroup_rows), use_container_width=True, hide_index=True)


def render_results(prediction, assessment) -> None:
    st.subheader("Risk Result")
    st.caption("Summarizes the patient-level triage score and the most influential model drivers.")
    result_a, result_b, result_c = st.columns(3)
    result_a.metric("PCOS triage risk", prediction.risk_tier)
    result_b.metric("Probability", f"{prediction.probability:.0%}")
    result_c.metric("Confidence", assessment.confidence)
    st.caption(f"Model tier used: {prediction.tier}")
    st.plotly_chart(probability_chart(prediction.probability), use_container_width=True)

    st.write("Top model drivers")
    driver_df = pd.DataFrame(prediction.top_drivers, columns=["Feature", "Contribution"])
    st.plotly_chart(driver_chart(prediction.top_drivers), use_container_width=True)
    st.dataframe(driver_df, use_container_width=True, hide_index=True)


def render_checklist(assessment) -> None:
    st.subheader("Guideline Checklist")
    st.caption("Translates the intake into clinical evidence areas instead of a black-box result.")
    rows = [
        {"Evidence area": item.name, "Status": item.status, "Notes": item.notes}
        for item in assessment.checklist
    ]
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    status_columns = st.columns(len(assessment.checklist))
    for column, item in zip(status_columns, assessment.checklist):
        with column:
            if item.status in {"Supported", "Present"}:
                st.success(item.status)
            elif item.status == "Caution":
                st.warning(item.status)
            elif item.status == "Incomplete":
                st.warning(item.status)
            else:
                st.info(item.status)
            st.caption(item.name)


def render_top_summary(prediction, assessment) -> None:
    summary = top_summary(prediction, assessment)
    st.subheader("Case Summary")
    metric_a, metric_b, metric_c, metric_d = st.columns(4)
    metric_a.metric("PCOS triage risk", summary["risk_tier"])
    metric_b.metric("Probability", summary["probability"])
    metric_c.metric("Model tier", summary["model_tier"])
    metric_d.metric("Confidence", summary["confidence"])
    st.success(f"Recommended next step: {summary['recommended_next_step']}")


def render_actions(patient, prediction, assessment) -> None:
    st.subheader("Next Action")
    st.caption("Groups the output into the pathway decision a clinician can act on next.")
    grouped = grouped_actions(assessment)

    action_a, action_b = st.columns(2)
    with action_a:
        st.write("PCOS pathway")
        for item in grouped["PCOS pathway"] or ["No PCOS-specific action from the current intake."]:
            st.success(item)

        st.write("Missing evidence")
        for item in grouped["Missing evidence"] or ["No missing evidence flagged from the current intake."]:
            st.warning(item)

    with action_b:
        st.write("Differential flags")
        for item in grouped["Differential flags"]:
            if item.startswith("No endometriosis"):
                st.info(item)
            else:
                st.warning(item)

        st.write("Recommended next step")
        for item in grouped["Recommended next step"] or ["Collect missing clinical evidence."]:
            st.success(item)

    st.subheader("Clinician Handoff")
    handoff = clinician_handoff_summary(
        patient,
        prediction.probability,
        prediction.risk_tier,
        prediction.tier,
        assessment,
    )
    st.text_area("Copy handoff summary for clinician-facing triage support", value=handoff, height=260)


def main() -> None:
    st.title("PCOS Navigator")
    st.info(SAFETY_STATEMENT)

    artifact = get_artifact()
    st.sidebar.header("Demo Case")
    case_name = st.sidebar.selectbox("Select case", list(DEMO_CASES.keys()))
    st.sidebar.info(CASE_EXPLANATIONS[case_name])
    st.sidebar.header("Demo Path")
    for index, (case, purpose) in enumerate(DEMO_PATH, start=1):
        st.sidebar.write(f"{index}. **{case}** - {purpose}")
    defaults = default_case_values(case_name)

    summary_container = st.container()

    tab_intake, tab_risk, tab_checklist, tab_evidence, tab_action = st.tabs(
        ["1 Intake", "2 Risk", "3 Checklist", "4 Evidence", "5 Action"]
    )
    with tab_intake:
        st.caption("Start here: choose a demo case, review patient inputs, and edit values if needed.")
        patient = patient_form(defaults)
        st.json({key: value for key, value in patient.items() if value is not None})

    tier = available_model_tier(patient)
    prediction = predict_patient(artifact, patient, tier)
    assessment = assess_patient(patient, prediction.probability, tier)

    with summary_container:
        render_top_summary(prediction, assessment)

    with tab_risk:
        render_results(prediction, assessment)
    with tab_checklist:
        render_checklist(assessment)
    with tab_evidence:
        render_model_evidence(artifact, prediction.tier)
    with tab_action:
        render_actions(patient, prediction, assessment)


if __name__ == "__main__":
    main()
