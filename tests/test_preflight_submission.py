from scripts.check_visual_evidence import check_visual_evidence
from scripts.preflight_submission import (
    CheckResult,
    CommandResult,
    check_generated_artifacts,
    command_results_to_markdown,
    preflight_to_markdown,
    summarize_export_bundle,
)
from pcos_navigator.config import SAFETY_STATEMENT


def test_command_result_formatting_outputs_pass_and_fail_rows():
    markdown = "\n".join(
        command_results_to_markdown(
            [
                CommandResult("Passing step", "uv run ok", "PASS", 0, "completed"),
                CommandResult("Failing step", "uv run bad", "FAIL", 1, "failed"),
            ]
        )
    )

    assert "| Passing step | `uv run ok` | PASS | 0 | completed |" in markdown
    assert "| Failing step | `uv run bad` | FAIL | 1 | failed |" in markdown


def test_preflight_report_contains_safety_app_demo_order_and_rubric_sections(tmp_path):
    screenshot_results = check_visual_evidence(tmp_path)
    report = preflight_to_markdown(
        [CommandResult("App import", 'uv run python -c "import app; print(\'app import ok\')"', "PASS", 0, "ok")],
        [CheckResult("reports/model_report.md", "PASS", "present")],
        [CheckResult("export folder", "PASS", "10 files exported")],
        screenshot_results,
    )

    assert SAFETY_STATEMENT in report
    assert "uv run streamlit run app.py" in report
    assert "Typical PCOS" in report
    assert "Incomplete Data" in report
    assert "Rubric-Facing Evidence" in report
    assert "Clinical validity" in report
    assert "Screenshot Evidence Status" in report


def test_missing_generated_artifacts_have_actionable_regeneration_messages(tmp_path):
    results = check_generated_artifacts(tmp_path)

    assert results
    assert any(result.status == "FAIL" for result in results)
    assert any("uv run python scripts/train_models.py" in result.detail for result in results)
    assert any("uv run python scripts/preflight_submission.py" in result.detail for result in results)


def test_export_summary_flags_blocked_files(tmp_path):
    export_dir = tmp_path / "pcos_navigator_presentation"
    export_dir.mkdir()
    (export_dir / "demo_script.md").write_text("# demo", encoding="utf-8")
    (export_dir / "unsafe.joblib").write_bytes(b"model")

    results = summarize_export_bundle(export_dir)

    assert any(result.label == "export blocked files" and result.status == "FAIL" for result in results)
