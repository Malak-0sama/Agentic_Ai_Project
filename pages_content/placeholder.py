"""Placeholder page renderer for routes not yet fully implemented in app2."""

from __future__ import annotations

import streamlit as st


def render_placeholder_page(label: str, module: str | None = None) -> None:
    st.title(label)
    st.markdown(
        f"""
        <div class="empty-state">
            <p>This page is wired in navigation and will be expanded in a later module.</p>
            <span class="module-tag">{module or "unassigned"}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption("Tip: use `streamlit run Home.py` for the full pipeline UI.")
