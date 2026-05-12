from pcos_navigator.config import MODEL_ARTIFACT_PATH, MODEL_METRICS_PATH, MODEL_REPORT_PATH
from pcos_navigator.data import load_clean_pcos
from pcos_navigator.modeling import save_artifacts, train_models


def main() -> None:
    df = load_clean_pcos()
    artifact, metrics = train_models(df)
    save_artifacts(artifact, metrics)
    print(f"Wrote {MODEL_ARTIFACT_PATH}")
    print(f"Wrote {MODEL_METRICS_PATH}")
    print(f"Wrote {MODEL_REPORT_PATH}")
    for tier, tier_metrics in metrics["tiers"].items():
        print(
            f"{tier}: AUROC={tier_metrics['auroc']:.3f}, "
            f"AUPRC={tier_metrics['auprc']:.3f}, "
            f"sensitivity={tier_metrics['sensitivity']:.3f}, "
            f"specificity={tier_metrics['specificity']:.3f}"
        )


if __name__ == "__main__":
    main()
