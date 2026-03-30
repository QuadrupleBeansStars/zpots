"""Navigation components for Player and Owner flows."""
import streamlit as st


def navigate(page_name, **kwargs):
    """Navigate to a page by setting session state and rerunning."""
    st.session_state.page = page_name
    for k, v in kwargs.items():
        st.session_state[k] = v
    st.rerun()


def render_player_topbar():
    """Render the player top navigation bar."""
    cols = st.columns([2, 1, 1, 1, 1, 1])
    with cols[0]:
        if st.button("**ZPOTS**", key="nav_logo", use_container_width=True):
            navigate("player_home")
    with cols[2]:
        if st.button("Explore", key="nav_explore"):
            navigate("player_home")
    with cols[3]:
        if st.button("My Bookings", key="nav_bookings"):
            navigate("my_bookings")
    with cols[4]:
        if st.button("Insights", key="nav_insights"):
            pass
    with cols[5]:
        st.markdown("🔔 &nbsp; 👤", unsafe_allow_html=True)


def render_owner_sidebar():
    """Render the owner sidebar navigation."""
    with st.sidebar:
        st.markdown("""
        <div style="padding: 0.5rem 0 1.5rem 0;">
            <span style="font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: 1.3rem; color: #272e42;">
                ZPOTS Admin
            </span><br>
            <span style="font-family: 'Lexend', sans-serif; font-size: 10px; text-transform: uppercase; letter-spacing: 0.1em; color: #535b71;">
                Elite Venue Partner
            </span>
        </div>
        """, unsafe_allow_html=True)

        menu_items = {
            "owner_dashboard": ("📊", "Dashboard"),
            "manage_courts": ("🏟", "Venue Manager"),
            "manage_slots": ("📅", "Slot Control"),
            "pricing_setup": ("💰", "Pricing"),
            "booking_dashboard": ("📋", "Booking Dashboard"),
            "ai_insights": ("🤖", "AI Ops"),
            "optimization": ("⚡", "Optimization"),
        }

        current_page = st.session_state.get("page", "owner_dashboard")

        for page_key, (icon, label) in menu_items.items():
            is_active = current_page == page_key
            bg = "background: linear-gradient(135deg, #cffc00, #e8ff66); color: #4b5e00; font-weight: 600;" if is_active else ""
            if st.button(
                f"{icon}  {label}",
                key=f"sidebar_{page_key}",
                use_container_width=True,
                type="primary" if is_active else "secondary",
            ):
                navigate(page_key)

        st.markdown("<br>" * 3, unsafe_allow_html=True)

        if st.button("➕ Add New Court", key="sidebar_add_court", type="primary", use_container_width=True):
            navigate("add_edit_court", editing_court_id=None)
