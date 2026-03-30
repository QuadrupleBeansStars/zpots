"""Player Home - Discover & Book Your Next Game."""
import streamlit as st
from components.css import inject_global_css
from components.nav import navigate, render_player_topbar
from components.cards import court_card
from data.dummy_data import COURTS


def render():
    inject_global_css()
    render_player_topbar()

    # Hero section
    st.markdown("""
    <div style="background: linear-gradient(135deg, #eef0ff 0%, #f6f6ff 100%); border-radius:20px; padding:3rem 2.5rem; margin-bottom:2rem; position:relative; overflow:hidden;">
        <span class="ai-tag" style="margin-bottom:12px;">AI-POWERED DISCOVERY</span>
        <h1 style="font-size:2.8rem; line-height:1.1; margin:0.8rem 0;">Discover & Book<br>Your Next Game<br><em style="color:#506300;">in Bangkok.</em></h1>
        <p style="color:#535b71; font-size:15px; max-width:500px; margin-top:0.8rem;">Find the best sports courts, choose your time, and join the action with real-time AI availability.</p>
    </div>
    """, unsafe_allow_html=True)

    bcol1, bcol2, bcol3 = st.columns([1, 1, 3])
    with bcol1:
        if st.button("Search Courts", type="primary", key="hero_search"):
            navigate("player_search")
    with bcol2:
        if st.button("Explore Sports", key="hero_explore"):
            navigate("player_search")

    st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)

    # Sport icons row
    sports = ["🏸", "⚽", "🏀", "🎾", "🏐", "🏓"]
    sport_cols = st.columns(len(sports))
    for i, sport in enumerate(sports):
        with sport_cols[i]:
            st.markdown(f"""
            <div style="text-align:center; padding:12px; background:white; border-radius:12px; font-size:1.5rem; cursor:pointer; box-shadow:0 2px 8px rgba(39,46,66,0.04);">
                {sport}
            </div>
            """, unsafe_allow_html=True)

    # Featured Courts
    st.markdown("<div style='height:2rem;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="display:flex; justify-content:space-between; align-items:center;">
        <div>
            <h2 style="font-size:1.5rem; margin:0;">Featured Courts</h2>
            <p style="color:#535b71; font-size:13px; margin-top:2px;">Top-rated venues chosen by the Bangkok community.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(4)
    for i, court in enumerate(COURTS[:4]):
        with cols[i]:
            court_card(court, key_prefix=f"home_court_{i}")

    # Master Your Game section
    st.markdown("<div style='height:2.5rem;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center; margin-bottom:1.5rem;">
        <h2 style="font-size:1.8rem;">Master Your Game in 3 Steps</h2>
        <p style="color:#535b71; font-size:14px;">Our streamlined process gets you on the court faster than ever before.</p>
    </div>
    """, unsafe_allow_html=True)

    step_cols = st.columns(3)
    steps = [
        ("🔍", "1. Search", "Browse local, nearby courts based on your sport, time, and budget preferences."),
        ("📅", "2. Book", "Select your preferred time slot and complete the booking in seconds."),
        ("🎮", "3. Play", "Show your QR code, check in, and enjoy your game with zero hassle."),
    ]
    for i, (icon, title, desc) in enumerate(steps):
        with step_cols[i]:
            st.markdown(f"""
            <div class="zpots-card" style="text-align:center; padding:2rem 1.5rem;">
                <div style="font-size:2.5rem; margin-bottom:1rem;">{icon}</div>
                <h3 style="font-size:1.1rem; margin-bottom:0.5rem;">{title}</h3>
                <p style="font-size:13px; color:#535b71;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    # AI Smart Booking section
    st.markdown("<div style='height:2rem;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="zpots-card-dark" style="padding:2rem 2.5rem;">
        <span class="ai-tag" style="background:rgba(207,252,0,0.1);">POWERED BY ZPOTS AI</span>
        <h2 style="color:white !important; font-size:1.8rem; margin-top:0.8rem;">Experience Precision<br>with <span style="color:#cffc00;">Smart Booking</span></h2>
        <ul style="color:rgba(255,255,255,0.8); font-size:14px; margin-top:1rem; list-style:none; padding:0;">
            <li style="margin-bottom:8px;">⚡ Dynamic pricing based on real-time court demand</li>
            <li style="margin-bottom:8px;">🎯 AI-suggested partners matching your skill level</li>
            <li style="margin-bottom:8px;">📊 Smart predictions & live availability tracking</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
