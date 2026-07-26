def build_insights_report_prompt(results):

    prompt = f"""
You are a senior Business Intelligence Analyst.

You are given the evaluation results of the BEST machine learning model selected automatically by the system.

Your task is to generate a professional business report based ONLY on the provided information.

Results:

{results}

----------------------------

Return ONLY valid JSON.

The JSON must contain exactly:

{{
    "executive_summary": "...",

    "key_insights": [
        "...",
        "...",
        "..."
    ],

    "model_performance": "...",

    "business_recommendations": [
        "...",
        "...",
        "..."
    ],

    "conclusion": "..."
}}

Rules:

- Return JSON only.
- No markdown.
- No `json.
- Do not invent values.
- Use only the metrics that exist.
- If a metric is missing, mention that it is unavailable.
- Explain the model performance in simple business language.
- Business recommendations must be realistic and actionable.
- Do not mention any information that is not included in the results.
- Keep the report concise and professional.

"""

    return prompt