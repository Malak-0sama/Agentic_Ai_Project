"""Agentic AI Platform — application entry point.

Run with:
    streamlit run app.py

This file stays intentionally thin: page config, CSS injection, sidebar
render, and routing to page content. No business logic lives here — that's
the whole point of the modular structure (see the architecture review and
the UI/UX blueprint for the full rationale).
"""

import streamlit as st

from config.navigation import NAV_HOME, find_page_label, find_page_module
from pages_content.dashboard_preview import render_dashboard_preview
from pages_content.placeholder import render_placeholder_page
from ui.sidebar import render_sidebar
from ui.styles import inject_global_css

st.set_page_config(
    page_title="Agentic AI Platform",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_global_css()

active_page = render_sidebar()

# --- Page router -----------------------------------------------------------
# Only the Dashboard route has real content in Module 1 (as a foundation
# preview). Every other route resolves to a styled placeholder that names
# the module it ships in, per the approved build sequence.
if active_page == NAV_HOME.key:
    render_dashboard_preview()
else:
    label = find_page_label(active_page) or active_page.replace("_", " ").title()
    module = find_page_module(active_page)
    render_placeholder_page(label, module)