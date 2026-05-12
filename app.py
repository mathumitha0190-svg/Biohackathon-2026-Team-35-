from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from pcos_navigator.clinical import assess_patient
from pcos_navigator.config import MODEL_ARTIFACT_PATH, SAFETY_STATEMENT
from pcos_navigator.data import available_model_tier, load_clean_pcos
from pcos_navigator.demo_cases import DEMO_CASES
from pcos_navigator.modeling import load_artifact, predict_patient, save_artifacts, train_models


st.set_page_config(
    page_title="PCOS Navigator",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_resource(show_spinner=False)
def get_artifact() -> dict:
    if MODEL_ARTIFACT_PATH.exists():
        return load_artifact()
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


def render_results(prediction, assessment) -> None:
    st.subheader("Risk Result")
    result_a, result_b, result_c = st.columns(3)
    result_a.metric("PCOS triage risk", prediction.risk_tier)
    result_b.metric("Probability", f"{prediction.probability:.0%}")
    result_c.metric("Confidence", assessment.confidence)
    st.caption(f"Model tier used: {prediction.tier}")
    st.plotly_chart(probability_chart(prediction.probability), use_container_width=True)

    st.write("Top model drivers")
    driver_df = pd.DataFrame(prediction.top_drivers, columns=["Feature", "Contribution"])
    st.dataframe(driver_df, use_container_width=True, hide_index=True)


def render_checklist(assessment) -> None:
    st.subheader("Guideline Checklist")
    rows = [
        {"Evidence area": item.name, "Status": item.status, "Notes": item.notes}
        for item in assessment.checklist
    ]
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)


def render_actions(assessment) -> None:
    st.subheader("Differential Flags")
    if assessment.differential_flags:
        for flag in assessment.differential_flags:
            st.warning(flag)
    else:
        st.info("No endometriosis-pattern red flags from the provided intake.")

    st.subheader("Next Best Action")
    for action in assessment.next_actions:
        st.success(action)


def main() -> None:
    st.title("PCOS Navigator")
    st.info(SAFETY_STATEMENT)

    artifact = get_artifact()
    st.sidebar.header("Demo Case")
    case_name = st.sidebar.selectbox("Select case", list(DEMO_CASES.keys()))
    defaults = default_case_values(case_name)

    tab_intake, tab_risk, tab_checklist, tab_action = st.tabs(
        ["Patient Intake", "Risk Result", "Guideline Checklist", "Next Action"]
    )
    with tab_intake:
        patient = patient_form(defaults)
        st.json({key: value for key, value in patient.items() if value is not None})

    tier = available_model_tier(patient)
    prediction = predict_patient(artifact, patient, tier)
    assessment = assess_patient(patient, prediction.probability, tier)

    with tab_risk:
        render_results(prediction, assessment)
    with tab_checklist:
        render_checklist(assessment)
    with tab_action:
        render_actions(assessment)


if __name__ == "__main__":
    main()
