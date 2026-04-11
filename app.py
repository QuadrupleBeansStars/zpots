"""ZPOTS - Sports Court Booking Platform."""
import streamlit as st

st.set_page_config(
    page_title="ZPOTS",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Import page renderers
from pages.player.login import render as player_login
from pages.player.home import render as player_home
from pages.player.search import render as player_search
from pages.player.court_details import render as court_details
from pages.player.booking import render as player_booking
from pages.player.confirmation import render as booking_confirmation
from pages.player.my_bookings import render as my_bookings
from pages.player.checkin import render as checkin_qr
from pages.player.feedback import render as leave_feedback

from pages.owner.login import render as owner_login
from pages.owner.dashboard import render as owner_dashboard
from pages.owner.manage_courts import render as manage_courts
from pages.owner.add_edit_court import render as add_edit_court
from pages.owner.manage_slots import render as manage_slots
from pages.owner.pricing import render as pricing_setup
from pages.owner.booking_dashboard import render as booking_dashboard
from pages.owner.ai_insights import render as ai_insights
from pages.owner.optimization import render as optimization

from components.css import inject_global_css

# Page registry
PAGE_REGISTRY = {
    "landing": None,  # handled inline
    "player_login": player_login,
    "player_home": player_home,
    "player_search": player_search,
    "court_details": court_details,
    "player_booking": player_booking,
    "booking_confirmation": booking_confirmation,
    "my_bookings": my_bookings,
    "checkin_qr": checkin_qr,
    "leave_feedback": leave_feedback,
    "owner_login": owner_login,
    "owner_dashboard": owner_dashboard,
    "manage_courts": manage_courts,
    "add_edit_court": add_edit_court,
    "manage_slots": manage_slots,
    "pricing_setup": pricing_setup,
    "booking_dashboard": booking_dashboard,
    "ai_insights": ai_insights,
    "optimization": optimization,
}

# Initialize session state
for key, default in [
    ("page", "landing"),
    ("flow", None),
    ("logged_in", False),
    ("selected_court_id", None),
    ("selected_booking_id", None),
    ("selected_slot_idx", None),
    ("editing_court_id", None),
]:
    if key not in st.session_state:
        st.session_state[key] = default


def render_landing():
    """Landing page - choose Player or Owner flow."""
    inject_global_css()

    # Hide sidebar on landing
    st.markdown("""
    <style>
    section[data-testid="stSidebar"] { display: none; }
    </style>
    """, unsafe_allow_html=True)

    st.space("large")

    with st.container(horizontal_alignment="center"):
        st.title("⚡ ZPOTS")
        st.write("AI-Powered Sports Court Booking Platform")

    st.space("medium")

    _, col2, _ = st.columns([1, 2, 1])
    with col2:
        left, right = st.columns(2, gap="medium")

        with left:
            with st.container(border=True):
                with st.container(horizontal_alignment="center"):
                    st.markdown("### 🏸")
                    st.subheader("I'm a Player")
                    st.caption("Discover courts, book sessions, and track your games in Bangkok.")
                st.space("small")
                if st.button("Enter as Player", type="primary", use_container_width=True, icon=":material/arrow_forward:", key="enter_player"):
                    st.session_state.page = "player_login"
                    st.session_state.flow = "player"
                    st.rerun()

        with right:
            with st.container(border=True):
                with st.container(horizontal_alignment="center"):
                    st.markdown("### 🏟")
                    st.subheader("I'm a Court Owner")
                    st.caption("Manage venues, optimize pricing, and grow your sports business.")
                st.space("small")
                if st.button("Enter as Owner", type="primary", use_container_width=True, icon=":material/arrow_forward:", key="enter_owner"):
                    st.session_state.page = "owner_login"
                    st.session_state.flow = "owner"
                    st.rerun()

    st.space("medium")
    with st.container(horizontal_alignment="center"):
        st.markdown('<span class="ai-tag">KINETIC PRECISION ENGINEERED</span>', unsafe_allow_html=True)


# Main routing
current_page = st.session_state.get("page", "landing")

if current_page == "landing":
    render_landing()
elif current_page in PAGE_REGISTRY and PAGE_REGISTRY[current_page] is not None:
    # Hide sidebar for login and player pages
    if current_page in ("player_login", "owner_login"):
        st.markdown('<style>section[data-testid="stSidebar"] { display: none; }</style>', unsafe_allow_html=True)
    elif st.session_state.flow == "player":
        st.markdown('<style>section[data-testid="stSidebar"] { display: none; }</style>', unsafe_allow_html=True)

    PAGE_REGISTRY[current_page]()
else:
    render_landing()
