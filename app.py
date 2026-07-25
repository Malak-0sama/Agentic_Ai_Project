import json

from agents.schema_agent import SchemaAgent
from agents.llm_planner_agent import LLMPlannerAgent


def print_section(title):
    print("\n" + "=" * 70)
    print(title.center(70))
    print("=" * 70)


def main():

    context = {
        "file_path": "C:\\Users\\workstation\\Desktop\\business-ai-agent\\uploads\\Sample - Superstore.csv"
    }

    
    schema_agent = SchemaAgent()

    context = schema_agent.run(context)

    print_section("SCHEMA SUMMARY")

    schema = context["schema"]

    dataset = schema["dataset"]

    print(f"Rows               : {dataset['rows']}")
    print(f"Columns            : {dataset['columns']}")
    print(f"Numeric Columns    : {dataset['numeric_columns']}")
    print(f"Categorical        : {dataset['categorical_columns']}")
    print(f"Datetime           : {dataset['datetime_columns']}")

    print()

    quality = schema["quality"]

    print(f"Quality Score      : {quality['quality_score']}")

   
    planner = LLMPlannerAgent()

    context = planner.run(context)

    print_section("EXECUTION PLAN")

    print(
        json.dumps(
            context["plan"],
            indent=4,
            ensure_ascii=False
        )
    )
if __name__ == "__main__":
    main()