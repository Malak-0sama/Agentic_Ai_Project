import json


def build_planner_prompt(schema: dict) -> str:

    schema_json = json.dumps(schema, indent=4)

    return f"""
You are a Senior Machine Learning Architect.

Your job is to analyze the dataset schema and generate a COMPLETE machine learning execution plan.

Dataset Schema:

{schema_json}

==========================
IMPORTANT RULES
==========================

1. Return ONLY valid JSON.
2. Do NOT use markdown.
3. Do NOT write explanations outside JSON.
4. Every preprocessing step MUST be represented as an operation.
5. Every feature engineering step MUST be represented as an operation.
6. Every operation MUST contain:
   - operation
   - parameters

==========================
AVAILABLE PREPROCESSING OPERATIONS
==========================

DROP_COLUMNS

CONVERT_DATETIME

FILL_MISSING_VALUES

REMOVE_DUPLICATES

ONE_HOT_ENCODING

LABEL_ENCODING

TARGET_ENCODING

FREQUENCY_ENCODING

STANDARD_SCALER

MINMAX_SCALER

ROBUST_SCALER

LOG_TRANSFORM

REMOVE_OUTLIERS

==========================
AVAILABLE FEATURE ENGINEERING OPERATIONS
==========================

CREATE_SHIPPING_DELAY

EXTRACT_YEAR

EXTRACT_MONTH

EXTRACT_DAY

EXTRACT_DAY_OF_WEEK

EXTRACT_QUARTER

CREATE_UNIT_PRICE

CREATE_INTERACTION_FEATURE

CREATE_RATIO_FEATURE

==========================
OUTPUT FORMAT
==========================

{{
    "target": {{
        "column": "...",
        "reason": "..."
    }},

    "task": {{
        "type": "...",
        "reason": "..."
    }},

    "preprocessing": [

        {{
            "operation": "DROP_COLUMNS",
            "parameters": {{
                "columns": [
                    "Row ID",
                    "Country"
                ]
            }}
        }}

    ],

    "feature_engineering": [

        {{
            "operation": "CREATE_SHIPPING_DELAY",
            "parameters": {{
                "order_date": "Order Date",
                "ship_date": "Ship Date"
            }}
        }}

    ],

    "recommended_models":[

        {{
            "name":"LightGBM",
            "priority":1
        }},

        {{
            "name":"CatBoost",
            "priority":2
        }}

    ],

    "evaluation":{{
        "metrics":[
            "MAE",
            "RMSE",
            "R2"
        ],
        "validation":"TimeSeriesSplit"
    }},

    "warnings":[
        "..."
    ],

    "recommendations":[
        "..."
    ],

    "reasoning":[
        "..."
    ],

    "confidence":0.95

}}

==========================
WHAT TO THINK ABOUT
==========================

- Detect the best target column.
- Detect whether the task is regression, classification, or clustering.
- Choose preprocessing operations.
- Choose feature engineering operations.
- Recommend the best ML models.
- Recommend evaluation metrics.
- Add warnings.
- Add recommendations.
- Explain your reasoning.
- Estimate confidence.

Return ONLY the JSON.
"""