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
    assert "uv run python scripts/check_readiness.py" in readme
    assert "uv run python scripts/check_visual_evidence.py" in readme
    assert "uv run python scripts/preflight_submission.py" in readme
    assert "uv run python scripts/preflight_submission.py --strict-screenshots" in readme
    assert "Typical PCOS" in readme
    assert (export_dir / "evidence_dossier.md").exists()
    assert (export_dir / "rubric_scorecard.md").exists()
    assert (export_dir / "visual_evidence_guide.md").exists()
    assert (export_dir / "final_demo_rehearsal.md").exists()


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


def test_export_includes_readiness_report_only_when_present(tmp_path):
    export_dir = export_presentation(tmp_path / "pcos_navigator_presentation")
    readiness_report = export_dir / "readiness_report.md"

    if Path("reports/readiness_report.md").exists():
        assert readiness_report.exists()
    else:
        assert not readiness_report.exists()


def test_export_includes_visual_evidence_report_only_when_present(tmp_path):
    export_dir = export_presentation(tmp_path / "pcos_navigator_presentation")
    visual_report = export_dir / "visual_evidence_report.md"

    if Path("reports/visual_evidence_report.md").exists():
        assert visual_report.exists()
    else:
        assert not visual_report.exists()


def test_export_includes_preflight_report_only_when_present(tmp_path):
    export_dir = export_presentation(tmp_path / "pcos_navigator_presentation")
    preflight_report = export_dir / "preflight_submission_report.md"

    if Path("reports/preflight_submission_report.md").exists():
        assert preflight_report.exists()
    else:
        assert not preflight_report.exists()


def test_export_copies_existing_screenshot_images(tmp_path, monkeypatch):
    screenshot_dir = tmp_path / "screenshots_source"
    screenshot_dir.mkdir()
    (screenshot_dir / "01_intake_summary.png").write_bytes(b"fake-png")
    monkeypatch.setattr("scripts.export_presentation.SCREENSHOTS_DIR", screenshot_dir)

    export_dir = export_presentation(tmp_path / "pcos_navigator_presentation")

    assert (export_dir / "screenshots" / "01_intake_summary.png").exists()
