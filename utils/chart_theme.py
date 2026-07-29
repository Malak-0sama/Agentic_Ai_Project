"""Shared Plotly theme for the Agentic AI Platform.

Every chart anywhere in the app must be passed through `apply_theme()` before
`st.plotly_chart(...)`. This is what keeps 20+ different pages visually
consistent instead of each page inventing its own chart style.

Usage:
    import plotly.express as px
    from utils.chart_theme import apply_theme, PLOTLY_CONFIG

    fig = px.line(df, x="date", y="value")
    apply_theme(fig)
    st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)
"""

from typing import Any, Dict

import plotly.graph_objects as go

from ui.theme import THEME

_c = THEME.color
_t = THEME.type

LAYOUT_DEFAULTS: Dict[str, Any] = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family=_t.font_ui, color=_c.text_secondary, size=13),
    colorway=list(THEME.chart_sequence),
    hoverlabel=dict(
        bgcolor=_c.bg_elevated,
        bordercolor=_c.accent_primary,
        font=dict(family=_t.font_mono, color=_c.text_primary, size=12),
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
        bgcolor="rgba(0,0,0,0)",
        bordercolor="rgba(0,0,0,0)",
        font=dict(size=12, color=_c.text_secondary),
    ),
    margin=dict(l=40, r=20, t=40, b=40),
    hovermode="x unified",
)

AXIS_DEFAULTS: Dict[str, Any] = dict(
    gridcolor=_c.border_subtle,
    zerolinecolor=_c.border_subtle,
    showline=False,
    tickfont=dict(family=_t.font_mono, size=11, color=_c.text_tertiary),
    title_font=dict(family=_t.font_ui, size=12, color=_c.text_secondary),
)

# Passed as `config=` to st.plotly_chart — trims the modebar to the actions
# a data-analysis user actually reaches for, per the chart design standard.
PLOTLY_CONFIG: Dict[str, Any] = {
    "displaylogo": False,
    "modeBarButtonsToRemove": [
        "select2d",
        "lasso2d",
        "autoScale2d",
        "hoverClosestCartesian",
        "hoverCompareCartesian",
        "toggleSpikelines",
    ],
    "displayModeBar": True,
    "responsive": True,
}


def apply_theme(fig: go.Figure, *, show_vertical_grid: bool = False, height: int = None) -> go.Figure:
    """Apply the platform's dark theme to a Plotly figure, in place.

    Args:
        fig: The Plotly figure to theme.
        show_vertical_grid: Vertical gridlines are off by default per the
            chart design standard (reduces visual noise); set True to opt in.
        height: Optional fixed height in pixels.

    Returns:
        The same figure, themed, for convenient chaining.
    """
    fig.update_layout(**LAYOUT_DEFAULTS)
    if height is not None:
        fig.update_layout(height=height)
    fig.update_xaxes(**AXIS_DEFAULTS, showgrid=show_vertical_grid)
    fig.update_yaxes(**AXIS_DEFAULTS, showgrid=True)
    return fig


def empty_state_figure(message: str, height: int = 260) -> go.Figure:
    """A themed placeholder figure for charts that have no data to show yet."""
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        showarrow=False,
        font=dict(family=_t.font_ui, size=14, color=_c.text_tertiary),
        xref="paper",
        yref="paper",
        x=0.5,
        y=0.5,
    )
    fig.update_layout(
        height=height,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
    )
    return apply_theme(fig)