"""Dashboard preview used by the alternate app2.py entry point."""

from __future__ import annotations

import streamlit as st


def render_dashboard_preview() -> None:
    st.title("Dashboard")
    st.caption(
        "Preview shell for the Agentic AI Platform. "
        "For the full multipage app, run: `streamlit run Home.py`"
    )
    st.info(
        "Upload a dataset and run the agent pipeline from **Home.py** "
        "(Dashboard → AI Workspace → Analytics & Reports)."
    )
