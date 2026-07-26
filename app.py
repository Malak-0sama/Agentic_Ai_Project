
import json
import pandas as pd
from agents.insights_report_agent import InsightsReportAgent
from agents.model_agent import ModelAgent
from agents.schema_agent import SchemaAgent
from agents.llm_planner_agent import LLMPlannerAgent
from agents.preprocessing_agent import PreprocessingAgent


DATASET_PATH = r"C:\Users\workstation\Desktop\business-ai-agent\uploads\Sample - Superstore.csv"


def load_dataset(path):

    encodings = [
        "utf-8",
        "utf-8-sig",
        "cp1252",
        "latin1",
    ]

    for enc in encodings:

        try:

            df = pd.read_csv(
                path,
                encoding=enc,
            )

            print(f"\nDataset loaded using {enc}")

            return df

        except UnicodeDecodeError:
            pass

    raise Exception("Cannot read dataset.")


def separator(title):

    print("\n")

    print("=" * 70)

    print(title.center(70))

    print("=" * 70)


def main():

    df = load_dataset(DATASET_PATH)

    context = {

        "dataframe": df

    }

    #######################################################

    schema_agent = SchemaAgent()

    context = schema_agent.run(context)

    schema = context["schema"]

    separator("SCHEMA SUMMARY")

    dataset = schema["dataset"]

    quality = schema["quality"]

    print("Rows :", dataset["rows"])

    print("Columns :", dataset["columns"])

    print("Numeric :", dataset["numeric_columns"])

    print("Categorical :", dataset["categorical_columns"])

    print("Datetime :", dataset["datetime_columns"])

    print()

    print("Quality :", quality["quality_score"])

    #######################################################

    planner = LLMPlannerAgent()

    context = planner.run(context)

    separator("EXECUTION PLAN")

    print(

        json.dumps(

            context["plan"],

            indent=4,

            ensure_ascii=False,

        )

    )

    #######################################################

    preprocessing = PreprocessingAgent()

    context = preprocessing.run(context)

    processed = context["processed_dataframe"]

    separator("PROCESSED DATASET")

    print(processed.head())

    print()

    print("Shape :", processed.shape)

    print()

    print(processed.info())

    separator("FINISHED")

    #######################################################

    #######################################################

    model_agent = ModelAgent()

    context = model_agent.run(context)

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

      metrics = result["metrics"]

      for metric, value in metrics.items():

        if isinstance(value, (int, float)):

            print(f"{metric:<15}: {value:.4f}")

           
   #######################################################

    separator("AI INSIGHTS REPORT")

    insights_agent = InsightsReportAgent()

    context = insights_agent.run(context)

    report = context["insights_report"]

    print("\n========== EXECUTIVE SUMMARY ==========\n")
    print(report["executive_summary"])

    print("\n========== KEY INSIGHTS ==========\n")

    for insight in report["key_insights"]:
        print("- " + insight)

    print("\n========== MODEL PERFORMANCE ==========\n")
    print(report["model_performance"])

    print("\n========== BUSINESS RECOMMENDATIONS ==========\n")

    for recommendation in report["business_recommendations"]:
        print("- " + recommendation)

    #######################################################

    separator("AI INSIGHTS REPORT")

    insights_agent = InsightsReportAgent()

    context = insights_agent.run(context)

    report = context["insights_report"]

    print("\n========== EXECUTIVE SUMMARY ==========\n")
    print(report["executive_summary"])

    print("\n========== KEY INSIGHTS ==========\n")

    for insight in report["key_insights"]:
        print("- " + insight)

    print("\n========== MODEL PERFORMANCE ==========\n")
    print(report["model_performance"])

    print("\n========== BUSINESS RECOMMENDATIONS ==========\n")

    for recommendation in report["business_recommendations"]:
        print("- " + recommendation)

    #######################################################

    separator("AI INSIGHTS REPORT")

    insights_agent = InsightsReportAgent()

    context = insights_agent.run(context)

    report = context["insights_report"]

    print("\n========== EXECUTIVE SUMMARY ==========\n")
    print(report["executive_summary"])

    print("\n========== KEY INSIGHTS ==========\n")

    for insight in report["key_insights"]:
        print("- " + insight)

    print("\n========== MODEL PERFORMANCE ==========\n")
    print(report["model_performance"])

    print("\n========== BUSINESS RECOMMENDATIONS ==========\n")

    for recommendation in report["business_recommendations"]:
        print("- " + recommendation)


     #######################################################

    separator("AI INSIGHTS REPORT")

    insights_agent = InsightsReportAgent()

    context = insights_agent.run(context)

    report = context["insights_report"]

    print("\n========== EXECUTIVE SUMMARY ==========\n")
    print(report["executive_summary"])

    print("\n========== KEY INSIGHTS ==========\n")

    for insight in report["key_insights"]:
        print("- " + insight)

    print("\n========== MODEL PERFORMANCE ==========\n")
    print(report["model_performance"])

    print("\n========== BUSINESS RECOMMENDATIONS ==========\n")

    for recommendation in report["business_recommendations"]:
        print("- " + recommendation)

    print("\n========== CONCLUSION ==========\n")
    print(report["conclusion"])

if __name__ == "__main__":

    main()