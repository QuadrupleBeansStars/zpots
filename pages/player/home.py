"""Player Home - Discover & Book Your Next Game."""
import streamlit as st
from components.css import inject_global_css
from components.nav import navigate, render_player_topbar
from components.cards import court_card
from data.dummy_data import COURTS


def render():
    inject_global_css()
    render_player_topbar()

    st.space("small")

    # Hero section
    with st.container(border=True):
        st.badge("AI-POWERED DISCOVERY", icon=":material/bolt:", color="green")
        st.title("Discover & Book\nYour Next Game")
        st.markdown("**in Bangkok** — find courts, choose your time, and join the action with real-time AI availability.")
        st.space("small")
        with st.container(horizontal=True):
            if st.button("Search Courts", type="primary", icon=":material/search:", key="hero_search"):
                navigate("player_search")
            if st.button("Explore Sports", icon=":material/explore:", key="hero_explore"):
                navigate("player_search")

    st.space("small")

    # Sport icons row
    sports = [("🏸", "Badminton"), ("⚽", "Football"), ("🏀", "Basketball"), ("🎾", "Tennis"), ("🏐", "Volleyball"), ("🏓", "Table Tennis")]
    sport_cols = st.columns(len(sports), gap="small")
    for i, (icon, label) in enumerate(sports):
        with sport_cols[i]:
            with st.container(border=True):
                with st.container(horizontal_alignment="center"):
                    st.markdown(f"#### {icon}")
                    st.caption(label)

    st.space("medium")

    # Featured Courts
    left_h, right_h = st.columns([3, 1], vertical_alignment="bottom")
    with left_h:
        st.subheader("Featured Courts")
        st.caption("Top-rated venues chosen by the Bangkok community.")
    with right_h:
        if st.button("View all", icon=":material/arrow_forward:", key="view_all_courts"):
            navigate("player_search")

    cols = st.columns(4, gap="small")
    for i, court in enumerate(COURTS[:4]):
        with cols[i]:
            court_card(court, key_prefix=f"home_court_{i}")

    st.space("medium")

    # Master Your Game section
    with st.container(horizontal_alignment="center"):
        st.subheader("Master Your Game in 3 Steps")
        st.caption("Our streamlined process gets you on the court faster than ever before.")

    st.space("small")

    step_cols = st.columns(3, gap="medium")
    steps = [
        (":material/search:", "1. Search", "Browse local courts based on your sport, time, and budget preferences."),
        (":material/calendar_month:", "2. Book", "Select your preferred time slot and complete the booking in seconds."),
        (":material/sports:", "3. Play", "Show your QR code, check in, and enjoy your game with zero hassle."),
    ]
    for i, (icon, title, desc) in enumerate(steps):
        with step_cols[i]:
            with st.container(border=True):
                with st.container(horizontal_alignment="center"):
                    st.markdown(f"#### {icon}")
                    st.subheader(title)
                    st.caption(desc)

    st.space("medium")

    # AI Smart Booking banner
    st.markdown("""
    <div class="zpots-card-dark" style="padding:2rem 2.5rem;">
        <span class="ai-tag" style="background:rgba(207,252,0,0.1);">POWERED BY ZPOTS AI</span>
        <h2 style="color:white !important; font-size:1.8rem; margin-top:0.8rem;">Experience Precision<br>with <span style="color:#cffc00;">Smart Booking</span></h2>
        <ul style="color:rgba(255,255,255,0.85); font-size:14px; margin-top:1rem; list-style:none; padding:0;">
            <li style="margin-bottom:8px;">⚡ Dynamic pricing based on real-time court demand</li>
            <li style="margin-bottom:8px;">🎯 AI-suggested partners matching your skill level</li>
            <li style="margin-bottom:8px;">📊 Smart predictions &amp; live availability tracking</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
