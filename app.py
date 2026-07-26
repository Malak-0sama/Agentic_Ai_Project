import json
import pandas as pd

from core.workflow import AgentWorkflow


def load_dataset(path):
    

    encodings = [
        "utf-8",
        "utf-8-sig",
        "cp1252",
        "latin1",
    ]

    for enc in encodings:
        try:
            df = pd.read_csv(path, encoding=enc)
            print(f"\nDataset loaded successfully using {enc}")
            return df

        except UnicodeDecodeError:
            continue

    raise Exception("Cannot read dataset.")


def separator(title):
    print("\n")
    print("=" * 70)
    print(title.center(70))
    print("=" * 70)


def main(dataset_path):
   

    
    df = load_dataset(dataset_path)

    
    workflow = AgentWorkflow()
    context = workflow.run(df)

    #######################################################

    separator("SCHEMA SUMMARY")

    schema = context["schema"]

    dataset = schema["dataset"]
    quality = schema["quality"]

    print(f"Rows          : {dataset['rows']}")
    print(f"Columns       : {dataset['columns']}")
    print(f"Numeric       : {dataset['numeric_columns']}")
    print(f"Categorical   : {dataset['categorical_columns']}")
    print(f"Datetime      : {dataset['datetime_columns']}")
    print()
    print(f"Quality Score : {quality['quality_score']}")

    #######################################################

    separator("EXECUTION PLAN")

    print(
        json.dumps(
            context["plan"],
            indent=4,
            ensure_ascii=False,
        )
    )

    #######################################################

    separator("PROCESSED DATASET")

    processed = context["processed_dataframe"]

    print(processed.head())

    print()

    print("Shape :", processed.shape)

    print()

    processed.info()

    #######################################################

    separator("BEST MODEL")

    best = context["best_model"]

    print(f"Model  : {best['model_name']}")
    print(f"Metric : {best['metric']}")
    print(f"Score  : {best['score']}")

    #######################################################

    separator("MODEL EVALUATION")

    results = context["evaluation_results"]

    for name, result in results.items():

        if name.startswith("_"):
            continue

        print("\n" + "-" * 50)
        print(name)
        print("-" * 50)

        print("Status :", result["status"])

        if result["status"] == "failed":
            print("Error :", result["error"])
            continue

        print("Training Time :", result["train_time"])
        print()

        for metric, value in result["metrics"].items():

            if isinstance(value, (int, float)):
                print(f"{metric:<20}: {value:.4f}")

    #######################################################

    separator("AI INSIGHTS REPORT")

    report = context["insights_report"]

    print("\n========== EXECUTIVE SUMMARY ==========\n")
    print(report["executive_summary"])

    print("\n========== KEY INSIGHTS ==========\n")

    for insight in report["key_insights"]:
        print(f"- {insight}")

    print("\n========== MODEL PERFORMANCE ==========\n")
    print(report["model_performance"])

    print("\n========== BUSINESS RECOMMENDATIONS ==========\n")

    for recommendation in report["business_recommendations"]:
        print(f"- {recommendation}")

    print("\n========== CONCLUSION ==========\n")
    print(report["conclusion"])

    return context


if __name__ == "__main__":

    main(
        r"C:\Users\workstation\Desktop\business-ai-agent\uploads\Sample - Superstore.csv"
    )