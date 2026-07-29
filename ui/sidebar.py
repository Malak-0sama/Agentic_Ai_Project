"""Sidebar rendering and page-routing state for the Agentic AI Platform.

Streamlit's built-in multipage nav (`pages/` directory) intentionally isn't
used here — it can't do grouped/accordion sections or a persistent status
strip, and ends up reading as a generic Streamlit app. Instead the sidebar is
rendered from `config/navigation.py` with plain `st.button` elements plus the
CSS in `ui/styles.py`, and the active page is tracked in `st.session_state`.
"""

import streamlit as st

from config.navigation import NAV_GROUPS, NAV_HOME, group_for_page
from ui.theme import THEME

_SESSION_KEY_ACTIVE_PAGE = "active_page"
_SESSION_KEY_OPEN_GROUPS = "open_nav_groups"


def _init_routing_state() -> None:
    if _SESSION_KEY_ACTIVE_PAGE not in st.session_state:
        st.session_state[_SESSION_KEY_ACTIVE_PAGE] = NAV_HOME.key

    if _SESSION_KEY_OPEN_GROUPS not in st.session_state:
        # Auto-expand whichever group contains the current page (or Data,
        # on first load, since it's the natural starting workflow).
        current_group = group_for_page(st.session_state[_SESSION_KEY_ACTIVE_PAGE])
        st.session_state[_SESSION_KEY_OPEN_GROUPS] = {current_group} if current_group else set()


def _navigate_to(page_key: str) -> None:
    st.session_state[_SESSION_KEY_ACTIVE_PAGE] = page_key
    parent = group_for_page(page_key)
    if parent:
        st.session_state[_SESSION_KEY_OPEN_GROUPS].add(parent)
    st.rerun()


def _toggle_group(group_key: str) -> None:
    open_groups: set = st.session_state[_SESSION_KEY_OPEN_GROUPS]
    if group_key in open_groups:
        open_groups.discard(group_key)
    else:
        open_groups.add(group_key)
    st.rerun()


def _nav_button(label: str, key: str, active: bool, *, indent: bool = False) -> None:
    """Render a single nav row.

    Active state uses Streamlit's native `type="primary"` button kind rather
    than a markdown wrapper div — `st.markdown` and `st.button` render as
    sibling elements, not parent/child, so a wrapper div can never scope CSS
    around a widget. `type="primary"` renders a real `kind="primary"`
    attribute on the button element, which `ui/styles.py` targets directly.
    """
    prefix = "\u00a0\u00a0\u00a0\u00a0" if indent else ""
    if st.button(
        f"{prefix}{label}",
        key=f"navbtn_{key}",
        use_container_width=True,
        type="primary" if active else "secondary",
    ):
        _navigate_to(key)


def render_sidebar() -> str:
    """Render the full sidebar and return the currently active page key."""
    _init_routing_state()
    active_page = st.session_state[_SESSION_KEY_ACTIVE_PAGE]
    open_groups: set = st.session_state[_SESSION_KEY_OPEN_GROUPS]

    with st.sidebar:
        # --- Brand ---
        st.markdown(
            f"""
            <div style="display:flex; align-items:center; gap:10px; padding: 4px 4px 16px 4px;">
                <div style="width:32px; height:32px; border-radius:8px;
                            background:{THEME.color.gradient_brand};
                            display:flex; align-items:center; justify-content:center;
                            font-weight:700; color:white; font-size:16px;">A</div>
                <div>
                    <div style="font-weight:700; font-size:15px; color:{THEME.color.text_primary};
                                line-height:1.1;">Agentic AI Platform</div>
                    <div style="font-size:11px; color:{THEME.color.text_tertiary};">Workspace: Default</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # --- Agent activity strip ---
        st.markdown(
            f"""
            <div class="agent-strip">
                <span class="status-badge idle"><span class="status-dot"></span>3 agents idle</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        # --- Home / Dashboard ---
        _nav_button(f"{NAV_HOME.icon}  {NAV_HOME.label}", NAV_HOME.key, active_page == NAV_HOME.key)

        # --- Grouped sections (accordion) ---
        for group in NAV_GROUPS:
            is_open = group.key in open_groups
            chevron = "▾" if is_open else "▸"
            if st.button(
                f"{chevron}  {group.icon}  {group.label}",
                key=f"navgroup_{group.key}",
                use_container_width=True,
            ):
                _toggle_group(group.key)

            if is_open:
                for page in group.pages:
                    _nav_button(page.label, page.key, active_page == page.key, indent=True)

        # --- Footer: settings + user ---
        st.markdown("<div style='flex-grow:1'></div>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div style="margin-top:24px; padding-top:12px; border-top:1px solid {THEME.color.border_subtle};
                        display:flex; align-items:center; gap:8px; font-size:13px; color:{THEME.color.text_secondary};">
                <div style="width:26px; height:26px; border-radius:50%; background:{THEME.color.bg_elevated};
                            border:1px solid {THEME.color.border_subtle}; display:flex; align-items:center;
                            justify-content:center; font-size:12px;">U</div>
                <span>User</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    return active_page