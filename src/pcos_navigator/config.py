from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
PCOS_WORKBOOK = PROJECT_ROOT / "(Main_Dataset)_PCOS_data_without_infertility.xlsx"
ENDOMETRIOSIS_CSV = PROJECT_ROOT / "(Supplementary_Dataset)_structured_endometriosis_data.csv"
MODELS_DIR = PROJECT_ROOT / "models"
REPORTS_DIR = PROJECT_ROOT / "reports"
MODEL_ARTIFACT_PATH = MODELS_DIR / "pcos_models.joblib"
DATA_PROFILE_PATH = REPORTS_DIR / "data_profile.md"
MODEL_METRICS_PATH = REPORTS_DIR / "model_metrics.json"
MODEL_REPORT_PATH = REPORTS_DIR / "model_report.md"
READINESS_REPORT_PATH = REPORTS_DIR / "readiness_report.md"

SAFETY_STATEMENT = (
    "This tool supports triage and investigation planning. It is not a diagnosis."
)
