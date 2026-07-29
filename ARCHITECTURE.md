# Architecture Overview (Phase 1)

## Source analyzed

`https://github.com/shimaiibrahim/Agentic_Ai_Project` (fork of
`Malak-0sama/Agentic_Ai_Project`, `main` branch).

## What exists in the repository today

```
agents/            Schema, Planning (LLM), Preprocessing, Model agents
                    + base_agent.py, tool_registry.py, planner_agent.py
config/             constants.py, llm_config.py, target_keywords.py
llm/                gemini_provider.py, provider.py
models/             evaluator.py, registry.py, splitter.py, trainer.py, validator.py
preprocessing/      package (contents not readable from this environment)
prompts/            planner_prompt.py
tools/              (contents not readable from this environment)
utils/              (contents not readable from this environment)
app.py              CLI entry point — NOT a Streamlit app
list_models.py      standalone script listing available Gemini models
requirements.txt    pipeline/ML dependencies only (no web framework except FastAPI+uvicorn)
test_gemini.py       Gemini connectivity smoke test
README.md           empty (0 bytes)
```

## Confirmed pipeline contract (from `app.py`)

```python
context = {"dataframe": df}
context = SchemaAgent().run(context)          # -> context["schema"]
context = LLMPlannerAgent().run(context)      # -> context["plan"]
context = PreprocessingAgent().run(context)   # -> context["processed_dataframe"]
context = ModelAgent().run(context)           # -> context["best_model"], context["evaluation_results"]
```

`context["schema"]` shape (from `app.py`'s own print statements):

```
schema["dataset"]["rows"]
schema["dataset"]["columns"]
schema["dataset"]["numeric_columns"]
schema["dataset"]["categorical_columns"]
schema["dataset"]["datetime_columns"]
schema["quality"]["quality_score"]
```

`context["evaluation_results"]` is a dict keyed by model name (keys
starting with `_` are treated as metadata, not a model), each value:

```
{"status": "success"|"failed", "error": str, "train_time": float, "metrics": {...}}
```

## What this build adds

A presentation layer only, calling the above contract as-is:

```
Home.py                          Dashboard (page 1)
pages/1_AI_Workspace.py          Pipeline runner UI (page 2)
pages/2_Analytics_Reports.py     Report + export UI (page 3)
ui/theme.py                      Dark glassmorphism CSS + components
services/pipeline_service.py     Wraps agent .run(context) calls with timing/error capture
services/report_service.py       Builds + exports the report (md/json/csv/pdf)
services/state.py                st.session_state schema shared across pages
```

No file inside `agents/`, `models/`, `llm/`, `preprocessing/`,
`prompts/`, or `tools/` was read in full or modified — see
`AUDIT.md` for exactly why, and what to double-check locally before
relying on this in production.

## Data flow

```
User uploads CSV (Dashboard)
        │
        ▼
st.session_state["dataset"]
        │
        ▼
AI Workspace: run_pipeline(df) ──▶ SchemaAgent ──▶ LLMPlannerAgent ──▶ PreprocessingAgent ──▶ ModelAgent
        │                                                                                        │
        ▼                                                                                        ▼
st.session_state["pipeline_context"]  ◀───────────────────────────────────────────────────────────┘
        │
        ▼
Analytics & Reports: build_report(context) ──▶ Markdown / JSON / CSV / PDF
```
