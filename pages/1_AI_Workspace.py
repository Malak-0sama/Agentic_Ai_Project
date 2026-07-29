"""
pages/1_AI_Workspace.py — AI Workspace (Page 2)
-------------------------------------------------
Runs the existing agent pipeline (Schema -> Planning -> Preprocessing
-> Model) against the uploaded dataset, rendering each step live:
progress, loading state, success/error badge, execution time, and
expandable logs. Uses st.status so Streamlit keeps re-rendering
between steps instead of freezing on one long call.
"""

import streamlit as st

from services.state import init_state
from services.pipeline_service import run_pipeline
from ui.theme import apply_page_config, inject_global_css, hero, badge, glass, render_sidebar

apply_page_config("AI Workspace", icon="🧠")
init_state()
inject_global_css()
render_sidebar(active="workspace")

hero("AI Workspace", "Run the full agentic pipeline on your dataset, step by step.")

df = st.session_state.get("dataset")

if df is None:
    glass("No dataset loaded yet. Go to <b>Dashboard</b> and upload a CSV first.")
    st.stop()

st.caption(f"Active dataset: **{st.session_state.get('dataset_name')}** — {df.shape[0]:,} rows × {df.shape[1]:,} columns")

run_col, reset_col = st.columns([1, 5])
with run_col:
    run_clicked = st.button("▶ Run pipeline", use_container_width=True)
with reset_col:
    if st.session_state.get("pipeline_ran") and st.button("↺ Reset run"):
        st.session_state["pipeline_context"] = None
        st.session_state["pipeline_steps"] = []
        st.session_state["pipeline_ran"] = False
        st.rerun()

status_badges = {
    "success": "success",
    "error": "error",
    "running": "warn",
    "pending": "idle",
    "skipped": "idle",
}

step_placeholders = {}

if run_clicked:
    step_names = ["Context Creation", "Schema Agent", "Planning Agent (LLM)",
                  "Preprocessing / Feature Engineering", "Model Recommendation"]
    for name in step_names:
        step_placeholders[name] = st.empty()
        step_placeholders[name].markdown(
            f'<div class="glass-card">⏳ <b>{name}</b> {badge("pending", "idle")}</div>',
            unsafe_allow_html=True,
        )

    def on_start(name: str) -> None:
        step_placeholders[name].markdown(
            f'<div class="glass-card">🔄 <b>{name}</b> {badge("running", "warn")}</div>',
            unsafe_allow_html=True,
        )

    def on_end(name: str, result) -> None:
        kind = status_badges.get(result.status, "idle")
        icon = {"success": "✅", "error": "❌", "skipped": "⏭️"}.get(result.status, "•")
        step_placeholders[name].markdown(
            f'<div class="glass-card">{icon} <b>{name}</b> '
            f'{badge(result.status, kind)} '
            f'<span style="color:#9AA3B2; font-size:0.85rem;"> — {result.duration_seconds:.2f}s</span></div>',
            unsafe_allow_html=True,
        )

    with st.spinner("Running agentic pipeline..."):
        context, results = run_pipeline(df, on_step_start=on_start, on_step_end=on_end)

    st.session_state["pipeline_context"] = context
    st.session_state["pipeline_steps"] = results
    st.session_state["pipeline_ran"] = True

# ---------------------------------------------------------------- Step details (always rendered if we have results)
results = st.session_state.get("pipeline_steps") or []
if results:
    st.markdown("#### Step details")
    for result in results:
        icon = {"success": "✅", "error": "❌", "skipped": "⏭️", "pending": "⏳"}.get(result.status, "•")
        with st.expander(f"{icon} {result.name} — {result.status} ({result.duration_seconds:.2f}s)"):
            if result.error:
                st.error(result.error)
            if result.logs:
                st.code("\n".join(result.logs), language="text")
            if not result.logs and not result.error:
                st.caption("No logs recorded for this step.")

    any_error = any(r.status == "error" for r in results)
    if any_error:
        st.warning(
            "The pipeline stopped at the first failing step. Fix the underlying agent/data issue "
            "and re-run — this preserves your original agent logic untouched; only the UI reports the failure."
        )
    else:
        st.success("Pipeline completed successfully. See **Analytics & Reports** for the full report.")

        context = st.session_state.get("pipeline_context") or {}
        best_model = context.get("best_model") or {}
        if best_model:
            glass(
                f"<b>Recommended model:</b> {best_model.get('model_name')} &nbsp;·&nbsp; "
                f"<b>{best_model.get('metric')}:</b> {best_model.get('score')}"
            )
elif not run_clicked:
    glass("Click <b>Run pipeline</b> to execute Context Creation → Schema → Planning → "
          "Preprocessing → Model Recommendation on this dataset.")
