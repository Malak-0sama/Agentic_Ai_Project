"""
services/diagnostics.py
-------------------------
Runtime health checks for the integration between this Streamlit UI
and the existing agent/model/llm packages.

This does NOT guess at what's inside those packages — it simply
attempts real imports and captures whatever Python actually raises,
so ModuleNotFoundError / ImportError / circular-import failures are
reported with their real message and traceback instead of crashing
the whole app on page load.
"""

from __future__ import annotations

import importlib
import traceback
from dataclasses import dataclass, field

# Every module the UI touches, directly or transitively, based on
# app.py's imports plus the folder names you listed. If any of these
# don't exist under these exact names in your checkout, that IS a
# real finding this check will surface — not a bug in this checker.
EXPECTED_MODULES: list[str] = [
    "agents.schema_agent",
    "agents.llm_planner_agent",
    "agents.preprocessing_agent",
    "agents.model_agent",
    "agents.base_agent",
    "agents.tool_registry",
    "agents.planner_agent",
    "agents.insights_report_agent",
    "config.constants",
    "config.llm_config",
    "config.target_keywords",
    "config.navigation",
    "llm.provider",
    "llm.gemini_provider",
    "models.evaluator",
    "models.registry",
    "models.splitter",
    "models.trainer",
    "models.validator",
    "preprocessing",
    "prompts.planner_prompt",
    "prompts.insights_report_prompt",
    "tools",
    "tools.process_tools",
    "utils",
    "utils.column_utils",
    "core.workflow",
]

REQUIRED_FOR_PIPELINE = [
    "agents.schema_agent",
    "agents.llm_planner_agent",
    "agents.preprocessing_agent",
    "agents.model_agent",
]


@dataclass
class ModuleCheck:
    module: str
    ok: bool
    error: str | None = None
    traceback_text: str | None = None
    required: bool = False


@dataclass
class DiagnosticsReport:
    checks: list[ModuleCheck] = field(default_factory=list)

    @property
    def all_ok(self) -> bool:
        return all(c.ok for c in self.checks)

    @property
    def required_ok(self) -> bool:
        return all(c.ok for c in self.checks if c.required)

    @property
    def failed(self) -> list[ModuleCheck]:
        return [c for c in self.checks if not c.ok]


def run_import_diagnostics() -> DiagnosticsReport:
    report = DiagnosticsReport()
    for module_name in EXPECTED_MODULES:
        required = module_name in REQUIRED_FOR_PIPELINE
        try:
            importlib.import_module(module_name)
            report.checks.append(ModuleCheck(module=module_name, ok=True, required=required))
        except Exception as exc:  # noqa: BLE001 - intentionally broad, this IS the check
            report.checks.append(
                ModuleCheck(
                    module=module_name,
                    ok=False,
                    error=f"{type(exc).__name__}: {exc}",
                    traceback_text=traceback.format_exc(),
                    required=required,
                )
            )
    return report
