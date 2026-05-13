from pathlib import Path

from pcos_navigator.config import SAFETY_STATEMENT
from scripts.export_presentation import DOC_FILENAMES, export_presentation


def test_export_presentation_bundle_includes_docs_and_readme(tmp_path):
    export_dir = export_presentation(tmp_path / "pcos_navigator_presentation")

    assert export_dir.exists()
    for filename in DOC_FILENAMES:
        assert (export_dir / filename).exists()

    readme = (export_dir / "README.md").read_text(encoding="utf-8")
    assert SAFETY_STATEMENT in readme
    assert "uv run streamlit run app.py" in readme
    assert "Typical PCOS" in readme


def test_export_presentation_excludes_data_and_model_files(tmp_path):
    export_dir = export_presentation(tmp_path / "pcos_navigator_presentation")
    blocked_suffixes = {".xlsx", ".csv", ".tar", ".joblib"}

    exported_files = [path for path in export_dir.rglob("*") if path.is_file()]
    assert exported_files
    assert not any(path.suffix.lower() in blocked_suffixes for path in exported_files)


def test_export_includes_model_report_only_when_present(tmp_path):
    export_dir = export_presentation(tmp_path / "pcos_navigator_presentation")
    model_report = export_dir / "model_report.md"

    if Path("reports/model_report.md").exists():
        assert model_report.exists()
    else:
        assert not model_report.exists()
