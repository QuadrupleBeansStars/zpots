"""Navigation components for Player and Owner flows."""
import streamlit as st


def _set_page(page_name, **kwargs):
    """Update session state to point at a new page. Safe to use as on_click callback;
    Streamlit auto-reruns after on_click handlers, so do NOT call st.rerun() here."""
    st.session_state.page = page_name
    for k, v in kwargs.items():
        st.session_state[k] = v


def navigate(page_name, **kwargs):
    """Navigate to a page by setting session state and rerunning.

    Use this for *direct* call sites (e.g. inside `if st.button(...):` blocks). For
    `on_click=` callbacks, use `_set_page` instead — calling st.rerun() inside a
    callback is a no-op and Streamlit warns about it.
    """
    _set_page(page_name, **kwargs)
    st.rerun()


def _logout():
    for key in ("logged_in", "user_id", "user_name", "user_email", "booking_persisted",
                "booking_court", "booking_slot", "booking_date_iso", "booking_date_str",
                "booking_txn_id", "booking_total_final", "booking_chat"):
        st.session_state.pop(key, None)
    st.session_state.page = "landing"
    st.session_state.flow = None


def render_player_topbar():
    """Render the player top navigation bar."""
    current = st.session_state.get("page", "player_home")

    cols = st.columns([2, 1, 1, 1, 0.5, 0.5])
    with cols[0]:
        if st.button("⚡ **ZPOTS**", key="nav_logo"):
            navigate("player_home")
    with cols[1]:
        active = current == "player_home"
        if st.button("Explore", icon=":material/explore:", key="nav_explore",
                     type="primary" if active else "secondary"):
            navigate("player_home")
    with cols[2]:
        active = current == "my_bookings"
        if st.button("Bookings", icon=":material/calendar_month:", key="nav_bookings",
                     type="primary" if active else "secondary"):
            navigate("my_bookings")
    with cols[3]:
        if st.button("Insights", icon=":material/insights:", key="nav_insights"):
            pass
    with cols[4]:
        st.button("", icon=":material/notifications:", key="nav_notif")
    with cols[5]:
        user_name = st.session_state.get("user_name", "")
        label = user_name[0].upper() if user_name else ""
        if st.button(label or "", icon=":material/person:", key="nav_profile"):
            _logout()
            st.rerun()


def render_owner_sidebar():
    """Render the owner sidebar navigation."""
    with st.sidebar:
        # Header
        st.markdown("""
        <div style="padding:8px 0 2px;">
            <span style="font-family:'Space Grotesk';font-weight:700;font-size:17px;
                         color:#fff;letter-spacing:0.05em;">⚡ ZPOTS Admin</span>
        </div>
        <div style="font-family:'Lexend';font-size:9px;letter-spacing:0.12em;
                    color:#CFFC00;text-transform:uppercase;margin-bottom:12px;">
            Elite Venue Partner
        </div>
        """, unsafe_allow_html=True)
        st.divider()

        menu_items = [
            ("owner_dashboard",   ":material/dashboard:",      "Dashboard"),
            ("manage_courts",     ":material/stadium:",        "Venue Manager"),
            ("manage_slots",      ":material/calendar_month:", "Slot Control"),
            ("pricing_setup",     ":material/payments:",       "Pricing"),
            ("booking_dashboard", ":material/list_alt:",       "Bookings"),
            ("ai_insights",       ":material/smart_toy:",      "AI Insights"),
            ("optimization",      ":material/bolt:",           "Optimization"),
        ]

        current_page = st.session_state.get("page", "owner_dashboard")
        for page_key, icon, label in menu_items:
            is_active = current_page == page_key
            st.button(
                label, icon=icon, key=f"sidebar_{page_key}",
                use_container_width=True,
                type="primary" if is_active else "secondary",
                on_click=_set_page, kwargs={"page_name": page_key},
            )

        st.markdown("<div style='min-height:40px;'></div>", unsafe_allow_html=True)

        st.button("Add New Court", icon=":material/add_circle:", key="sidebar_add_court",
                  type="primary", use_container_width=True,
                  on_click=_set_page,
                  kwargs={"page_name": "add_edit_court", "editing_court_id": None})
        st.divider()
        st.button("Back to home", icon=":material/logout:", key="sidebar_logout",
                  use_container_width=True,
                  on_click=_logout)
