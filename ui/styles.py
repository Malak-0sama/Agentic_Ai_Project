"""Global stylesheet for the Agentic AI Platform.

The CSS is generated from `THEME` (config/theme.py) rather than hardcoded, so
there is exactly one place to change a color or a duration. `inject_global_css()`
is called once per page load from `app.py`.

Streamlit's default chrome (hamburger menu, "Made with Streamlit" footer,
default header) is stripped here so the app reads as a standalone product
rather than a Streamlit-hosted script.
"""

import streamlit as st

from ui.theme import THEME


def _build_css() -> str:
    c = THEME.color
    t = THEME.type
    m = THEME.motion
    s = THEME.space

    return f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* ---------- Reset / base ---------- */
    html, body, [class*="css"] {{
        font-family: {t.font_ui};
    }}

    #MainMenu, footer, header[data-testid="stHeader"] {{
        visibility: hidden;
        height: 0;
    }}

    .stApp {{
        background-color: {c.bg_primary};
        color: {c.text_primary};
    }}

    .block-container {{
        padding-top: {s.lg};
        padding-bottom: {s.xl};
        max-width: 1400px;
    }}

    ::-webkit-scrollbar {{ width: 8px; height: 8px; }}
    ::-webkit-scrollbar-track {{ background: {c.bg_surface}; }}
    ::-webkit-scrollbar-thumb {{ background: {c.border_focus}; border-radius: {s.radius_sm}; }}
    ::-webkit-scrollbar-thumb:hover {{ background: {c.accent_primary}; }}

    /* ---------- Typography ---------- */
    h1, h2, h3, h4, h5, h6 {{
        font-family: {t.font_ui};
        font-weight: {t.weight_semibold};
        color: {c.text_primary};
        letter-spacing: -0.01em;
    }}

    p, span, label, div {{
        color: {c.text_secondary};
    }}

    code, pre, .mono {{
        font-family: {t.font_mono} !important;
    }}

    /* ---------- Sidebar ---------- */
    section[data-testid="stSidebar"] {{
        background-color: {c.bg_surface};
        border-right: 1px solid {c.border_subtle};
    }}

    section[data-testid="stSidebar"] .block-container {{
        padding-top: {s.md};
    }}

    /* Sidebar nav buttons rendered via st.button — styled to look like a
       real product nav list rather than default Streamlit buttons. */
    section[data-testid="stSidebar"] button {{
        background-color: transparent !important;
        border: 1px solid transparent !important;
        color: {c.text_secondary} !important;
        text-align: left !important;
        font-weight: {t.weight_medium} !important;
        border-radius: {s.radius_sm} !important;
        transition: background-color {m.duration_fast} {m.ease_out},
                    border-color {m.duration_fast} {m.ease_out},
                    color {m.duration_fast} {m.ease_out};
        width: 100%;
        justify-content: flex-start !important;
    }}

    section[data-testid="stSidebar"] button:hover {{
        background-color: {c.bg_elevated} !important;
        color: {c.text_primary} !important;
        border-color: {c.border_focus} !important;
    }}

    section[data-testid="stSidebar"] button:focus:not(:active) {{
        border-color: {c.accent_primary} !important;
    }}

    /* Active nav item — driven by Streamlit's native type="primary" button
       kind (see ui/sidebar.py), which renders a real kind="primary"
       attribute we can target directly, rather than a markup hack. */
    section[data-testid="stSidebar"] button[kind="primary"] {{
        background-color: {c.bg_elevated} !important;
        color: {c.text_primary} !important;
        border-left: 3px solid {c.accent_primary} !important;
        box-shadow: inset 0 0 0 1px {c.border_focus};
    }}

    section[data-testid="stSidebar"] button[kind="primary"]:hover {{
        border-color: {c.accent_primary} !important;
    }}

    .nav-group-label {{
        font-size: 11px;
        font-weight: {t.weight_semibold};
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: {c.text_tertiary};
        padding: {s.md} {s.sm} {s.xs} {s.sm};
    }}

    /* ---------- Header bar ---------- */
    .app-header {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding-bottom: {s.lg};
        margin-bottom: {s.lg};
        border-bottom: 1px solid {c.border_subtle};
        animation: fadeSlideIn {m.duration_panel} {m.ease_out};
    }}

    .app-header .title {{
        font-size: {t.size_display};
        font-weight: {t.weight_bold};
        color: {c.text_primary};
        margin: 0;
    }}

    .app-header .subtitle {{
        font-size: {t.size_body};
        color: {c.text_secondary};
        margin-top: 2px;
    }}

    /* ---------- Cards ---------- */
    .card {{
        background-color: {c.bg_elevated};
        border: 1px solid {c.border_subtle};
        border-radius: {s.radius_md};
        padding: {s.lg};
        transition: border-color {m.duration_base} {m.ease_out},
                    transform {m.duration_base} {m.ease_out},
                    box-shadow {m.duration_base} {m.ease_out};
    }}

    .card:hover {{
        border-color: {c.border_focus};
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
    }}

    .glass-panel {{
        background: {c.bg_glass};
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid {c.border_subtle};
        border-radius: {s.radius_lg};
        padding: {s.lg};
    }}

    /* ---------- KPI metric card ---------- */
    .metric-card {{
        background-color: {c.bg_elevated};
        border: 1px solid {c.border_subtle};
        border-radius: {s.radius_md};
        padding: {s.lg};
        transition: border-color {m.duration_base} {m.ease_out},
                    transform {m.duration_base} {m.ease_out};
        animation: fadeSlideIn {m.duration_panel} {m.ease_out};
    }}

    .metric-card:hover {{
        border-color: {c.accent_primary};
        transform: translateY(-2px);
    }}

    .metric-card .metric-label {{
        font-size: {t.size_caption};
        color: {c.text_secondary};
        font-weight: {t.weight_medium};
        margin-bottom: {s.xs};
    }}

    .metric-card .metric-value {{
        font-family: {t.font_mono};
        font-size: 28px;
        font-weight: {t.weight_semibold};
        color: {c.text_primary};
        line-height: 1.2;
    }}

    .metric-card .metric-delta {{
        font-family: {t.font_mono};
        font-size: 12px;
        font-weight: {t.weight_medium};
        margin-top: {s.xs};
    }}

    .metric-delta.positive {{ color: {c.accent_success}; }}
    .metric-delta.negative {{ color: {c.accent_error}; }}
    .metric-delta.neutral {{ color: {c.text_tertiary}; }}

    /* ---------- Status badges ---------- */
    .status-badge {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 10px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: {t.weight_medium};
        font-family: {t.font_mono};
        border: 1px solid transparent;
    }}

    .status-dot {{
        width: 7px;
        height: 7px;
        border-radius: 50%;
        display: inline-block;
    }}

    .status-badge.idle {{ background: rgba(92,98,112,0.15); color: {c.text_tertiary}; }}
    .status-badge.idle .status-dot {{ background: {c.text_tertiary}; }}

    .status-badge.running {{ background: rgba(0,212,184,0.12); color: {c.accent_secondary}; }}
    .status-badge.running .status-dot {{ background: {c.accent_secondary}; animation: pulse 1.4s infinite; }}

    .status-badge.completed {{ background: rgba(61,220,151,0.12); color: {c.accent_success}; }}
    .status-badge.completed .status-dot {{ background: {c.accent_success}; }}

    .status-badge.failed {{ background: rgba(255,92,122,0.12); color: {c.accent_error}; }}
    .status-badge.failed .status-dot {{ background: {c.accent_error}; }}

    .status-badge.queued {{ background: rgba(255,176,32,0.12); color: {c.accent_warning}; }}
    .status-badge.queued .status-dot {{ background: {c.accent_warning}; }}

    /* ---------- Buttons ---------- */
    .stButton > button[kind="primary"], .stDownloadButton > button {{
        background: {c.gradient_brand};
        border: none;
        color: white;
        font-weight: {t.weight_semibold};
        border-radius: {s.radius_sm};
        transition: filter {m.duration_fast} {m.ease_out},
                    transform {m.duration_fast} {m.ease_out};
    }}

    .stButton > button[kind="primary"]:hover, .stDownloadButton > button:hover {{
        filter: brightness(1.1);
        transform: translateY(-1px);
    }}

    /* ---------- Skeleton loader ---------- */
    .skeleton {{
        background: linear-gradient(90deg, {c.bg_elevated} 25%, {c.border_subtle} 50%, {c.bg_elevated} 75%);
        background-size: 200% 100%;
        animation: shimmer 1.4s infinite;
        border-radius: {s.radius_sm};
    }}

    /* ---------- Placeholder / empty state ---------- */
    .empty-state {{
        text-align: center;
        padding: {s.xl} {s.lg};
        border: 1px dashed {c.border_subtle};
        border-radius: {s.radius_md};
        color: {c.text_tertiary};
        font-size: {t.size_body};
    }}

    .empty-state .module-tag {{
        display: inline-block;
        margin-top: {s.sm};
        font-family: {t.font_mono};
        font-size: 11px;
        color: {c.accent_primary};
        border: 1px solid {c.accent_primary};
        border-radius: 999px;
        padding: 2px 10px;
    }}

    /* ---------- Agent activity strip (sidebar) ---------- */
    .agent-strip {{
        display: flex;
        align-items: center;
        gap: 8px;
        padding: {s.sm} {s.md};
        margin: {s.sm} 0;
        background-color: {c.bg_elevated};
        border: 1px solid {c.border_subtle};
        border-radius: {s.radius_sm};
        font-size: 12px;
        color: {c.text_secondary};
    }}

    /* ---------- Animations ---------- */
    @keyframes fadeSlideIn {{
        from {{ opacity: 0; transform: translateY(8px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    @keyframes pulse {{
        0%   {{ box-shadow: 0 0 0 0 rgba(0,212,184,0.5); }}
        70%  {{ box-shadow: 0 0 0 6px rgba(0,212,184,0); }}
        100% {{ box-shadow: 0 0 0 0 rgba(0,212,184,0); }}
    }}

    @keyframes shimmer {{
        0%   {{ background-position: 200% 0; }}
        100% {{ background-position: -200% 0; }}
    }}
    </style>
    """


def inject_global_css() -> None:
    """Inject the platform stylesheet into the current Streamlit page.

    Call once, near the top of `app.py`, after `st.set_page_config`.
    """
    st.markdown(_build_css(), unsafe_allow_html=True)