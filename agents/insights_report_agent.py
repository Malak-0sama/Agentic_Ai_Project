import json

from agents.base_agent import BaseAgent
from llm.gemini_provider import GeminiProvider
from prompts.insights_report_prompt import build_insights_report_prompt


class InsightsReportAgent(BaseAgent):

    def __init__(self):
        self.llm = GeminiProvider()

    def run(self, context):

        evaluation = context["evaluation_results"]
        best = context["best_model"]
        plan = context["plan"]

        best_model_name = best["model_name"]

        best_result = evaluation[best_model_name]

        metrics = best_result["metrics"]

        results = {
            "model": best_model_name,
            "task": plan["task"]["type"],
            "primary_metric": best["metric"],
            "primary_score": best["score"],
        }

        for key, value in metrics.items():

            if isinstance(value, (int, float)):
                results[key] = value

        prompt = build_insights_report_prompt(results)

        response = self.llm.generate(prompt)

        response = (
            response.strip()
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        try:
            insights_report = json.loads(response)

        except json.JSONDecodeError:

            print(response)
            raise

        context["insights_report"] = insights_report

        return context