"""
services/report_service.py

Builds a professional executive report from the pipeline context.

Priority:
1. Use AI generated report from InsightsReportAgent (context["report"])
2. Add dataset/model metadata from pipeline context
3. Provide exports: JSON, Markdown, CSV, PDF
"""

from __future__ import annotations

import io
import json
from datetime import datetime, timezone
from typing import Any


def safe_get(data, *keys, default=None):
    """
    Safely retrieves nested dictionary values.
    """
    current = data

    for key in keys:
        if not isinstance(current, dict):
            return default

        current = current.get(key)

        if current is None:
            return default

    return current


def build_report(context: dict[str, Any]) -> dict[str, Any]:
    """
    Build final report object.

    Uses InsightsReportAgent output if available.
    """

    ai_report = context.get("report", {}) or {}

    schema = context.get("schema", {}) or {}
    dataset = schema.get("dataset", {}) or {}
    quality = schema.get("quality", {}) or {}

    best_model = context.get("best_model", {}) or {}

    evaluation_results = context.get(
        "evaluation_results",
        {}
    ) or {}


    model_rows = []

    for model_name, result in evaluation_results.items():

        if not isinstance(result, dict):
            continue

        row = {
            "model": model_name,
            "status": result.get("status")
        }


        metrics = result.get(
            "metrics",
            {}
        ) or {}


        for metric, value in metrics.items():

            if isinstance(value, (int, float)):
                row[metric] = round(value, 4)


        model_rows.append(row)



    report = {

        "generated_at":
            datetime.now(timezone.utc).isoformat(),


        "dataset_overview": {

            "rows":
                dataset.get("rows"),

            "columns":
                dataset.get("columns"),

            "numeric_columns":
                dataset.get("numeric_columns"),

            "categorical_columns":
                dataset.get("categorical_columns"),

            "datetime_columns":
                dataset.get("datetime_columns"),

            "quality_score":
                quality.get("quality_score")

        },


        "model_recommendation": {

            "best_model":
                best_model.get("model_name"),

            "metric":
                best_model.get("metric"),

            "score":
                best_model.get("score")

        },


        "model_evaluations":
            model_rows,


        "technical_report":
            ai_report.get(
                "technical_report",
                {}
            ),


        "business_report":
            ai_report.get(
                "business_report",
                {}
            ),


        "execution_plan":
            context.get(
                "plan",
                {}
            )

    }


    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),

        "dataset_overview": {
            "rows": dataset.get("rows"),
            "columns": dataset.get("columns"),
            "numeric_columns": dataset.get("numeric_columns"),
            "categorical_columns": dataset.get("categorical_columns"),
            "datetime_columns": dataset.get("datetime_columns"),
            "quality_score": quality.get("quality_score"),
            "processed_shape": list(processed_df.shape)
            if processed_df is not None else None,
        },

        "execution_plan": plan,


        "model_recommendation": {
            "best_model": best_model.get("model_name"),
            "metric": best_model.get("metric"),
            "score": best_model.get("score"),
        },


        "technical_report": ai_report.get(
            "technical_report",
            {}
        ),


        "business_report": ai_report.get(
            "business_report",
            {}
        ),


        "training_summary": training_summary,

        "model_evaluations": model_rows,

        "feature_importance": feature_importance,
    }



def to_markdown(report: dict[str, Any]) -> str:

    technical = report.get(
        "technical_report",
        {}
    )

    business = report.get(
        "business_report",
        {}
    )


    lines = [

        "# AI Business Intelligence Report",

        f"Generated: {report.get('generated_at')}",

        "",


        "## Executive Summary",

        business.get(
            "executive_summary",
            "Not available"
        ),


        "",

        "## Current Company Status",

        business.get(
            "current_company_status",
            ""
        ),


        "",

        "## Technical Report",

        "",


        f"Model: {safe_get(technical,'model_information','model_name')}",

        f"Problem Type: {safe_get(technical,'model_information','problem_type')}",

        f"Target Variable: {safe_get(technical,'model_information','target_variable')}",


        "",


        technical.get(
            "model_performance_summary",
            ""
        ),



        "",

        "## Technical Findings"

    ]


    for item in technical.get(
        "technical_findings",
        []
    ):

        lines.append(
            f"- {item}"
        )



    lines += [

        "",

        "## Technical Risks"

    ]


    for item in technical.get(
        "technical_risks",
        []
    ):

        lines.append(
            f"- {item}"
        )



    lines += [

        "",

        "## Technical Improvements"

    ]


    for item in technical.get(
        "technical_improvements",
        []
    ):

        lines.append(
            f"- {item}"
        )



    lines += [

        "",

        "## Business Analysis",

        "",


        "### KPI Analysis"

    ]


    kpi = business.get(
        "business_kpi_analysis",
        {}
    )


    for key,value in kpi.items():

        lines.append(
            f"- {key}: {value}"
        )



    lines += [

        "",

        "### Sales and Profit Drivers"

    ]


    for item in business.get(
        "sales_and_profit_drivers",
        []
    ):

        lines.append(
            f"- {item}"
        )



    lines += [

        "",

        "### Business Risks"

    ]


    for risk in business.get(
        "business_risks",
        []
    ):

        lines.append(
            f"- {risk}"
        )



    lines += [

        "",

        "### Business Opportunities"

    ]


    for opp in business.get(
        "business_opportunities",
        []
    ):

        lines.append(
            f"- {opp}"
        )



    lines += [

        "",

        "## Management Decisions"

    ]


    for decision in business.get(
        "management_decisions",
        []
    ):

        lines.append(
            f"""
Decision:
{decision.get('decision')}

Reason:
{decision.get('reason')}

Expected Value:
{decision.get('expected_business_value')}
"""
        )



    lines += [

        "",

        "## Future Strategy"

    ]


    for item in business.get(
        "future_strategy",
        []
    ):

        lines.append(
            f"- {item}"
        )



    lines += [

        "",

        "## Final Executive Conclusion",

        business.get(
            "final_executive_conclusion",
            ""
        )

    ]


    return "\n".join(lines)




def to_json_bytes(report):

    return json.dumps(
        report,
        indent=2,
        ensure_ascii=False,
        default=str
    ).encode(
        "utf-8"
    )



def to_csv_bytes(report):

    import csv


    output = io.StringIO()


    rows = report.get(
        "model_evaluations",
        []
    )


    if not rows:

        return b""


    writer = csv.DictWriter(
        output,
        fieldnames=rows[0].keys()
    )


    writer.writeheader()

    writer.writerows(rows)


    return output.getvalue().encode(
        "utf-8"
    )



def to_pdf_bytes(report):

    try:

        from fpdf import FPDF

    except ImportError:

        return None


    try:

        pdf = FPDF()

        pdf.add_page()

        pdf.set_auto_page_break(
            True,
            margin=15
        )


        pdf.set_font(
            "Helvetica",
            size=11
        )


        text = to_markdown(report)


        for line in text.split("\n"):

            pdf.multi_cell(
                0,
                6,
                line.encode(
                    "latin-1",
                    errors="replace"
                ).decode(
                    "latin-1"
                )
            )


        output = pdf.output(
            dest="S"
        )


        return bytes(output)



    except Exception:

        return None