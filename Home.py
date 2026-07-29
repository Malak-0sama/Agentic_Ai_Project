"""
Home.py — Dashboard (Page 1)
-----------------------------
Entry point for the Streamlit multipage app. Run with:

    streamlit run Home.py

Shows: project overview, dataset upload + stats, missing values,
dtypes, correlation summary, preview table, and an at-a-glance
workflow diagram of the agent pipeline.
"""

import pandas as pd
import plotly.express as px
import streamlit as st

from services.state import init_state
from services.diagnostics import run_import_diagnostics
from ui.theme import apply_page_config, inject_global_css, hero, kpi_card, glass, badge, render_sidebar

apply_page_config("Dashboard", icon="📊")
init_state()
inject_global_css()
render_sidebar(active="dashboard")

# ---------------------------------------------------------------- Hero
hero(
    "Dashboard",
    "Overview of your dataset, data quality, and the agentic pipeline ready to run on it.",
)

# ---------------------------------------------------------------- System diagnostics
with st.expander("🩺 System diagnostics — module import health", expanded=False):
    diag = run_import_diagnostics()
    if diag.all_ok:
        st.markdown(badge("All modules import cleanly", "success"), unsafe_allow_html=True)
    elif diag.required_ok:
        st.markdown(
            badge("Required modules OK — some optional modules failed", "warn"),
            unsafe_allow_html=True,
        )
    else:
        st.markdown(badge("Required module import failures detected", "error"), unsafe_allow_html=True)

    for check in diag.checks:
        icon = "✅" if check.ok else ("❌" if check.required else "⚠️")
        label = f"{icon} `{check.module}`" + ("" if check.ok else f" — {check.error}")
        st.markdown(label)
        if not check.ok and check.required:
            with st.expander(f"Traceback: {check.module}", expanded=False):
                st.code(check.traceback_text or "", language="text")

    if not diag.required_ok:
        st.error(
            "The pipeline cannot run until the required modules above import "
            "successfully. Run `python scripts/smoke_test.py` locally for the "
            "same check outside Streamlit."
        )

# ---------------------------------------------------------------- Upload
upload_col, info_col = st.columns([2, 1])
with upload_col:
    uploaded = st.file_uploader("Upload a CSV dataset", type=["csv"], key="dashboard_uploader")
    if uploaded is not None:
        try:
            from services.pipeline_service import load_dataset

            df = load_dataset(uploaded)
            st.session_state["dataset"] = df
            st.session_state["dataset_name"] = uploaded.name
            # New dataset invalidates any previous pipeline run.
            st.session_state["pipeline_context"] = None
            st.session_state["pipeline_steps"] = []
            st.session_state["pipeline_ran"] = False
        except Exception as exc:  # noqa: BLE001
            st.error(f"Could not read this file: {exc}")

with info_col:
    glass(
        """
        <b>Supported format</b><br/>CSV (encoding auto-detected: utf-8, utf-8-sig, cp1252, latin1)<br/><br/>
        <b>Next step</b><br/>Head to <b>AI Workspace</b> to run the full agent pipeline on this dataset.
        """
    )

df: pd.DataFrame | None = st.session_state.get("dataset")

if df is None:
    st.markdown("&nbsp;")
    glass(
        "<b>No dataset loaded.</b> Upload a CSV above to see live statistics, "
        "correlation analysis, and a preview here."
    )
    st.stop()

# ---------------------------------------------------------------- KPI cards
missing_total = int(df.isna().sum().sum())
missing_pct = (missing_total / (df.shape[0] * df.shape[1]) * 100) if df.size else 0.0
numeric_cols = df.select_dtypes(include="number").columns.tolist()
categorical_cols = df.select_dtypes(exclude="number").columns.tolist()

k1, k2, k3, k4 = st.columns(4)
with k1:
    st.markdown(kpi_card("Rows", f"{df.shape[0]:,}"), unsafe_allow_html=True)
with k2:
    st.markdown(kpi_card("Columns", f"{df.shape[1]:,}"), unsafe_allow_html=True)
with k3:
    good = missing_pct < 5
    st.markdown(
        kpi_card("Missing values", f"{missing_pct:.1f}%", f"{missing_total:,} cells", good=good),
        unsafe_allow_html=True,
    )
with k4:
    st.markdown(kpi_card("Numeric / Categorical", f"{len(numeric_cols)} / {len(categorical_cols)}"), unsafe_allow_html=True)

st.markdown("&nbsp;")

# ---------------------------------------------------------------- Dtypes + missingness chart
c1, c2 = st.columns(2)
with c1:
    st.markdown("#### Column data types")
    dtype_counts = df.dtypes.astype(str).value_counts().reset_index()
    dtype_counts.columns = ["dtype", "count"]
    fig = px.bar(dtype_counts, x="dtype", y="count", color="dtype", template="plotly_dark")
    fig.update_layout(showlegend=False, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.markdown("#### Missing values by column")
    missing_by_col = df.isna().sum().sort_values(ascending=False)
    missing_by_col = missing_by_col[missing_by_col > 0]
    if missing_by_col.empty:
        glass("No missing values detected in this dataset. 🎉")
    else:
        fig2 = px.bar(
            x=missing_by_col.values,
            y=missing_by_col.index,
            orientation="h",
            template="plotly_dark",
            labels={"x": "Missing count", "y": "Column"},
        )
        fig2.update_layout(margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------------------------------------- Correlation summary
st.markdown("#### Correlation summary (numeric columns)")
MAX_CORR_COLUMNS = 30  # keeps the heatmap responsive on memory-constrained deployments
if len(numeric_cols) >= 2:
    corr_cols = numeric_cols
    truncated = False
    if len(numeric_cols) > MAX_CORR_COLUMNS:
        # Show the columns with the highest variance rather than an
        # arbitrary slice, so the truncation still surfaces the most
        # informative relationships instead of just the first N columns.
        corr_cols = df[numeric_cols].var(numeric_only=True).sort_values(ascending=False).head(MAX_CORR_COLUMNS).index.tolist()
        truncated = True

    corr = df[corr_cols].corr(numeric_only=True)
    show_text = len(corr_cols) <= 20  # text_auto on 30x30+ cells is unreadable and slow to render
    fig3 = px.imshow(
        corr,
        text_auto=".2f" if show_text else False,
        color_continuous_scale="Purples", template="plotly_dark", aspect="auto",
    )
    fig3.update_layout(margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig3, use_container_width=True)
    if truncated:
        st.caption(f"Showing the {MAX_CORR_COLUMNS} highest-variance numeric columns of {len(numeric_cols)} total.")
else:
    glass("Need at least 2 numeric columns to compute a correlation matrix.")

# ---------------------------------------------------------------- Preview table
st.markdown("#### Dataset preview")
st.dataframe(df.head(50), use_container_width=True, height=320)

# ---------------------------------------------------------------- Workflow overview
st.markdown("#### Agent workflow")
steps = [
    "Context Creation", "Schema Agent", "Planning Agent", "Reasoning",
    "Feature Engineering", "EDA", "ML Recommendation", "Visualization", "Final Report",
]
cols = st.columns(len(steps))
for col, step in zip(cols, steps):
    with col:
        st.markdown(
            f'<div class="kpi-card" style="text-align:center; padding:0.8rem 0.4rem;">'
            f'<div style="font-size:0.78rem; color:#9AA3B2;">{step}</div></div>',
            unsafe_allow_html=True,
        )
st.caption("Run this pipeline end-to-end on the **AI Workspace** page.")