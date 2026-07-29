"""
services/state.py
-------------------
Single place that defines and initializes st.session_state keys used
across the Dashboard, AI Workspace, and Analytics & Reports pages, so
an uploaded dataset and pipeline results persist as the user navigates.
"""

import streamlit as st

DEFAULTS = {
    "dataset": None,          # pandas.DataFrame
    "dataset_name": None,     # str
    "pipeline_context": None, # dict returned by run_pipeline
    "pipeline_steps": [],     # list[StepResult]
    "pipeline_ran": False,
}


def init_state() -> None:
    for key, value in DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = value
