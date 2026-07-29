"""
ui/theme.py
------------
Central design system for the platform: page config, global CSS
(dark glassmorphism), and small reusable component builders.

Nothing here touches agents/, models/, llm/, preprocessing/, prompts/,
or tools/ — this module is presentation-only.
"""

from __future__ import annotations

import streamlit as st

from types import SimpleNamespace

PRIMARY = "#7C5CFF"
PRIMARY_2 = "#22D3EE"
BG_0 = "#0B0E14"
BG_1 = "#11151F"
CARD = "rgba(255,255,255,0.045)"
BORDER = "rgba(255,255,255,0.09)"
TEXT = "#E7E9EE"
MUTED = "#9AA3B2"
GOOD = "#34D399"
WARN = "#FBBF24"
BAD = "#F87171"

# Shared theme object used by ui/styles.py, ui/sidebar.py, and
# utils/chart_theme.py (alternate UI modules). Values align with the
# glassmorphism palette already used by Home.py / inject_global_css.
THEME = SimpleNamespace(
    color=SimpleNamespace(
        bg_primary=BG_0,
        bg_surface=BG_1,
        bg_elevated="#161B26",
        bg_glass=CARD,
        text_primary=TEXT,
        text_secondary=MUTED,
        text_tertiary="#6B7280",
        border_subtle=BORDER,
        border_focus="rgba(124,92,255,0.45)",
        accent_primary=PRIMARY,
        accent_secondary=PRIMARY_2,
        accent_success=GOOD,
        accent_warning=WARN,
        accent_error=BAD,
        gradient_brand=f"linear-gradient(135deg, {PRIMARY}, {PRIMARY_2})",
    ),
    type=SimpleNamespace(
        font_ui="'Inter', 'Segoe UI', system-ui, sans-serif",
        font_mono="'JetBrains Mono', 'Consolas', monospace",
        weight_medium=500,
        weight_semibold=600,
        weight_bold=700,
        size_display="1.75rem",
        size_body="0.95rem",
        size_caption="0.8rem",
    ),
    motion=SimpleNamespace(
        duration_fast="120ms",
        duration_base="180ms",
        duration_panel="220ms",
        ease_out="cubic-bezier(0.16, 1, 0.3, 1)",
    ),
    space=SimpleNamespace(
        xs="0.25rem",
        sm="0.5rem",
        md="0.75rem",
        lg="1.25rem",
        xl="2rem",
        radius_sm="8px",
        radius_md="14px",
        radius_lg="18px",
    ),
    chart_sequence=(
        PRIMARY,
        PRIMARY_2,
        GOOD,
        WARN,
        "#A78BFA",
        "#F472B6",
        "#38BDF8",
        "#FB7185",
    ),
)


def apply_page_config(page_title: str, icon: str = "🧠") -> None:
    st.set_page_config(
        page_title=f"{page_title} · Agentic AI Platform",
        page_icon=icon,
        layout="wide",
        initial_sidebar_state="expanded",
    )


def inject_global_css() -> None:
    st.markdown(
        f"""
        <style>
        /* Hide default Streamlit chrome */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}
        div[data-testid="stToolbar"] {{visibility: hidden;}}
        div[data-testid="stDecoration"] {{display: none;}}
        a[href*="streamlit.io"] {{display: none !important;}}

        html, body, [class*="css"] {{
            font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
        }}

        .stApp {{
            background:
                radial-gradient(1200px 600px at 10% -10%, rgba(124,92,255,0.16), transparent 60%),
                radial-gradient(1000px 500px at 100% 0%, rgba(34,211,238,0.12), transparent 55%),
                {BG_0};
            color: {TEXT};
        }}

        section[data-testid="stSidebar"] {{
            background: linear-gradient(180deg, {BG_1}, {BG_0});
            border-right: 1px solid {BORDER};
        }}

        section[data-testid="stSidebar"] .stRadio label {{
            font-size: 0.95rem;
        }}

        /* Glass card */
        .glass-card {{
            background: {CARD};
            border: 1px solid {BORDER};
            border-radius: 18px;
            padding: 1.25rem 1.4rem;
            backdrop-filter: blur(14px);
            -webkit-backdrop-filter: blur(14px);
            box-shadow: 0 8px 32px rgba(0,0,0,0.35);
            margin-bottom: 1rem;
        }}

        .gradient-border {{
            position: relative;
            border-radius: 18px;
            padding: 1px;
            background: linear-gradient(135deg, {PRIMARY}, {PRIMARY_2});
        }}
        .gradient-border > div {{
            background: {BG_1};
            border-radius: 17px;
        }}

        .hero-header {{
            padding: 2rem 2.2rem;
            border-radius: 22px;
            background: linear-gradient(120deg, rgba(124,92,255,0.20), rgba(34,211,238,0.10));
            border: 1px solid {BORDER};
            margin-bottom: 1.6rem;
        }}
        .hero-title {{
            font-size: 2rem;
            font-weight: 800;
            margin: 0;
            background: linear-gradient(90deg, #fff, {PRIMARY_2});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .hero-subtitle {{
            color: {MUTED};
            margin-top: 0.35rem;
            font-size: 1.02rem;
        }}

        /* KPI card */
        .kpi-card {{
            background: {CARD};
            border: 1px solid {BORDER};
            border-radius: 16px;
            padding: 1rem 1.2rem;
            transition: transform .15s ease, border-color .15s ease;
        }}
        .kpi-card:hover {{
            transform: translateY(-3px);
            border-color: rgba(124,92,255,0.5);
        }}
        .kpi-label {{
            color: {MUTED};
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: .06em;
        }}
        .kpi-value {{
            font-size: 1.7rem;
            font-weight: 750;
            margin-top: 0.2rem;
        }}
        .kpi-delta-good {{ color: {GOOD}; font-size: 0.82rem; }}
        .kpi-delta-bad {{ color: {BAD}; font-size: 0.82rem; }}

        /* Status badge */
        .badge {{
            display: inline-block;
            padding: 0.15rem 0.65rem;
            border-radius: 999px;
            font-size: 0.75rem;
            font-weight: 600;
            letter-spacing: .02em;
        }}
        .badge-success {{ background: rgba(52,211,153,0.15); color: {GOOD}; border: 1px solid rgba(52,211,153,0.35); }}
        .badge-warn {{ background: rgba(251,191,36,0.15); color: {WARN}; border: 1px solid rgba(251,191,36,0.35); }}
        .badge-error {{ background: rgba(248,113,113,0.15); color: {BAD}; border: 1px solid rgba(248,113,113,0.35); }}
        .badge-idle {{ background: rgba(154,163,178,0.12); color: {MUTED}; border: 1px solid rgba(154,163,178,0.3); }}

        /* Buttons */
        .stButton > button {{
            border-radius: 12px;
            border: 1px solid {BORDER};
            background: linear-gradient(135deg, {PRIMARY}, {PRIMARY_2});
            color: #08090c;
            font-weight: 700;
            padding: 0.55rem 1.2rem;
            transition: transform .12s ease, filter .12s ease;
        }}
        .stButton > button:hover {{
            transform: translateY(-1px);
            filter: brightness(1.08);
        }}

        div[data-testid="stExpander"] {{
            background: {CARD};
            border: 1px solid {BORDER};
            border-radius: 14px;
        }}

        hr {{ border-color: {BORDER}; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def hero(title: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div class="hero-header">
            <p class="hero-title">{title}</p>
            <p class="hero-subtitle">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def kpi_card(label: str, value: str, delta: str | None = None, good: bool = True) -> str:
    delta_html = ""
    if delta:
        cls = "kpi-delta-good" if good else "kpi-delta-bad"
        delta_html = f'<div class="{cls}">{delta}</div>'
    return f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            {delta_html}
        </div>
    """


def render_sidebar(active: str) -> None:
    """
    Single source of truth for the sidebar nav, used by Home.py and
    every page. `active` is one of "dashboard" | "workspace" | "reports"
    purely for a possible future active-state style — navigation itself
    is identical on every page, which is exactly why it belongs here
    instead of being duplicated in each file.
    """
    import streamlit as st  # local import avoids a hard dependency for callers that only need CSS/constants

    with st.sidebar:
        st.markdown("### 🧠 Agentic AI Platform")
        st.caption("Enterprise dataset intelligence & AutoML")
        st.divider()
        st.page_link("Home.py", label="Dashboard", icon="📊")
        st.page_link("pages/1_AI_Workspace.py", label="AI Workspace", icon="🧠")
        st.page_link("pages/2_Analytics_Reports.py", label="Analytics & Reports", icon="📈")
        st.divider()
        if st.session_state.get("dataset") is not None:
            st.success(f"Dataset loaded: {st.session_state['dataset_name']}")
        else:
            st.info("No dataset loaded yet.")


def badge(text: str, kind: str = "idle") -> str:
    return f'<span class="badge badge-{kind}">{text}</span>'


def glass(content_html: str) -> None:
    st.markdown(f'<div class="glass-card">{content_html}</div>', unsafe_allow_html=True)
