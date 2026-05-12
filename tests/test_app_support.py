from app import driver_chart
from pcos_navigator.data import available_model_tier, load_clean_pcos
from pcos_navigator.demo_cases import DEMO_CASES
from pcos_navigator.modeling import predict_patient, train_models


def test_driver_chart_uses_prediction_contributions():
    df = load_clean_pcos()
    artifact, _ = train_models(df)
    patient = DEMO_CASES["Typical PCOS"]
    prediction = predict_patient(artifact, patient, available_model_tier(patient))
    figure = driver_chart(prediction.top_drivers)

    assert prediction.top_drivers
    assert figure.data
    assert len(figure.data[0].x) == len(prediction.top_drivers)
