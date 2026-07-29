"""
services/pipeline_service.py
-----------------------------

Wraps the agentic pipeline:

SchemaAgent
        ↓
LLMPlannerAgent
        ↓
PreprocessingAgent
        ↓
ModelAgent
        ↓
InsightsReportAgent

Responsible for:
- Running agents sequentially
- Maintaining shared context
- Reporting execution status
- Loading uploaded datasets
"""

from __future__ import annotations

import hashlib
import time
import traceback

from dataclasses import dataclass, field
from typing import Any, Callable

import pandas as pd
import streamlit as st


from agents.schema_agent import SchemaAgent
from agents.llm_planner_agent import LLMPlannerAgent
from agents.preprocessing_agent import PreprocessingAgent
from agents.model_agent import ModelAgent
from agents.insights_report_agent import InsightsReportAgent



CANDIDATE_METHODS = (
    "run",
    "execute",
    "process"
)



@dataclass
class StepResult:

    name: str

    status: str = "pending"

    duration_seconds: float = 0.0

    error: str | None = None

    logs: list[str] = field(
        default_factory=list
    )

    method_used: str | None = None





PIPELINE_STEPS = [

    (
        "Context Creation",
        None
    ),


    (
        "Schema Agent",
        SchemaAgent
    ),


    (
        "Planning Agent (LLM)",
        LLMPlannerAgent
    ),


    (
        "Preprocessing / Feature Engineering",
        PreprocessingAgent
    ),


    (
        "Model Recommendation",
        ModelAgent
    ),


    (
        "Business Insights Report Agent",
        InsightsReportAgent
    )

]






@st.cache_resource(
    show_spinner=False
)
def _get_agent_instance(agent_cls):

    return agent_cls()






def _call_agent(agent, context):

    for method_name in CANDIDATE_METHODS:

        method = getattr(
            agent,
            method_name,
            None
        )


        if callable(method):

            return (
                method(context),
                method_name
            )



    if callable(agent):

        return (
            agent(context),
            "__call__"
        )



    raise AttributeError(
        f"{type(agent).__name__} has no valid execution method"
    )







def run_pipeline(
    df: pd.DataFrame,
    on_step_start: Callable[[str], None] | None = None,
    on_step_end: Callable[[str, StepResult], None] | None = None,
):


    context = {

        "dataframe": df,

        "original_dataframe": df.copy()

    }



    results = []

    failed = False




    for name, agent_cls in PIPELINE_STEPS:


        result = StepResult(
            name=name
        )



        if failed:

            result.status = "skipped"

            results.append(
                result
            )

            continue





        if on_step_start:

            on_step_start(
                name
            )



        result.status = "running"



        start = time.perf_counter()



        try:


            if agent_cls is None:


                result.logs.append(
                    f"Dataset loaded successfully: {df.shape}"
                )



            else:


                agent = _get_agent_instance(
                    agent_cls
                )



                context, method_used = _call_agent(
                    agent,
                    context
                )



                result.method_used = method_used



                result.logs.append(
                    f"{agent_cls.__name__}.{method_used}() completed."
                )



                if agent_cls == InsightsReportAgent:


                    result.logs.append(
                        "AI Business Report generated successfully."
                    )



            result.status = "success"





        except Exception as exc:


            result.status = "error"


            result.error = (
                f"{type(exc).__name__}: {exc}"
            )


            result.logs.append(
                traceback.format_exc()
            )


            failed = True






        finally:


            result.duration_seconds = (
                time.perf_counter()
                -
                start
            )





        results.append(
            result
        )



        if on_step_end:

            on_step_end(
                name,
                result
            )





    return (
        context,
        results
    )








def _read_csv_bytes(raw_bytes):

    import io


    encodings = [

        "utf-8",

        "utf-8-sig",

        "cp1252",

        "latin1"

    ]



    last_error = None



    for enc in encodings:


        try:


            return pd.read_csv(
                io.BytesIO(raw_bytes),
                encoding=enc
            )



        except Exception as exc:


            last_error = exc



    raise ValueError(
        f"Cannot read dataset. Last error: {last_error}"
    )








@st.cache_data(
    show_spinner=False
)
def _cached_read_csv_bytes(
    raw_bytes,
    _cache_key
):

    return _read_csv_bytes(
        raw_bytes
    )








def load_dataset(uploaded_file):


    uploaded_file.seek(
        0
    )


    raw_bytes = uploaded_file.read()



    cache_key = hashlib.sha256(
        raw_bytes
    ).hexdigest()



    return _cached_read_csv_bytes(
        raw_bytes,
        cache_key
    )