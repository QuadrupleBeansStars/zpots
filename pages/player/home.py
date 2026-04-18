"""Player Home - Discover & Book Your Next Game."""
import streamlit as st
from components.css import inject_global_css
from components.nav import navigate, render_player_topbar
from components.cards import court_card
from data.dummy_data import COURTS


def render():
    inject_global_css()
    render_player_topbar()

    st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)

    # ── Hero ──────────────────────────────────────────────────────────────
    st.markdown("""
    <div style="background:#fff;padding:2.5rem 0 1rem;">
        <div style="display:inline-flex;align-items:center;gap:6px;
                    background:rgba(207,252,0,0.18);border-radius:999px;
                    padding:4px 12px;margin-bottom:14px;">
            <span style="width:6px;height:6px;background:#CFFC00;border-radius:50%;
                         box-shadow:0 0 8px #CFFC00;display:inline-block;"></span>
            <span class="eyebrow" style="color:#2E6B00;">AI-Powered Discovery</span>
        </div>
        <h1 style="font-family:'Space Grotesk';font-size:2.8rem;font-weight:700;
                   line-height:1.0;letter-spacing:-0.02em;color:#1c2526;">
            Discover &amp; Book<br>Your Next Game</h1>
        <p style="color:#3d4455;font-size:15px;margin-top:10px;max-width:520px;line-height:1.5;">
            Find the best sports courts, choose your time, and join the action
            with real-time AI availability.</p>
    </div>
    """, unsafe_allow_html=True)

    hero_col1, hero_col2, _ = st.columns([1, 1, 3])
    with hero_col1:
        if st.button("Search Courts", type="primary", icon=":material/search:",
                     key="hero_search", width='stretch'):
            navigate("player_search")
    with hero_col2:
        if st.button("Explore Sports", icon=":material/explore:",
                     key="hero_explore", width='stretch'):
            navigate("player_search")

    st.markdown("<div style='height:1.5rem;'></div>", unsafe_allow_html=True)

    # ── Sport Row ─────────────────────────────────────────────────────────
    sports = [
        ("🏸","Badminton"), ("⚽","Football"), ("🏀","Basketball"),
        ("🎾","Tennis"),    ("🏐","Volleyball"), ("🏓","Table Tennis"),
    ]
    sport_cols = st.columns(len(sports))
    for i, (emoji, label) in enumerate(sports):
        with sport_cols[i]:
            st.markdown(f"""
            <div style="display:flex;flex-direction:column;align-items:center;gap:8px;">
                <div style="width:48px;height:48px;border-radius:50%;background:#F2F9EE;
                            display:flex;align-items:center;justify-content:center;">
                    <span style="font-size:22px;">{emoji}</span>
                </div>
                <span class="eyebrow" style="font-size:9px;">{label}</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:2rem;'></div>", unsafe_allow_html=True)

    # ── Featured Courts ───────────────────────────────────────────────────
    left_h, right_h = st.columns([3, 1], vertical_alignment="bottom")
    with left_h:
        st.markdown('<h2 style="font-family:\'Space Grotesk\';font-size:24px;font-weight:700;margin:0;">Featured Courts</h2>',
                    unsafe_allow_html=True)
        st.caption("Top-rated venues chosen by the Bangkok community.")
    with right_h:
        if st.button("View all →", key="view_all_courts"):
            navigate("player_search")

    cols = st.columns(4, gap="small")
    for i, court in enumerate(COURTS[:4]):
        with cols[i]:
            court_card(court, key_prefix=f"home_court_{i}")

    st.markdown("<div style='height:2.5rem;'></div>", unsafe_allow_html=True)

    # ── 3 Steps ───────────────────────────────────────────────────────────
    st.markdown("""
    <div style="text-align:center;margin-bottom:1rem;">
        <h2 style="font-family:'Space Grotesk';font-size:24px;font-weight:700;margin:0;">
            Master Your Game in 3 Steps</h2>
        <p style="color:#3d4455;font-size:13px;margin-top:4px;">
            Our streamlined process gets you on the court faster than ever before.</p>
    </div>
    """, unsafe_allow_html=True)

    step_cols = st.columns(3, gap="medium")
    steps = [
        ("search",         "1. Search", "Browse local courts based on your sport, time, and budget preferences."),
        ("calendar_month", "2. Book",   "Select your preferred time slot and complete the booking in seconds."),
        ("sports",         "3. Play",   "Show your QR code, check in, and enjoy your game with zero hassle."),
    ]
    for i, (icon, title, desc) in enumerate(steps):
        with step_cols[i]:
            st.markdown(f"""
            <div style="background:#fff;border:1px solid #E3F0DE;border-radius:16px;
                        padding:24px;text-align:center;">
                <div style="width:48px;height:48px;margin:0 auto 10px;border-radius:50%;
                            background:#F2F9EE;display:flex;align-items:center;justify-content:center;">
                    <span class="material-symbols-rounded"
                          style="font-size:24px;color:#2E6B00;">{icon}</span>
                </div>
                <h3 style="font-family:'Space Grotesk';font-size:17px;font-weight:600;
                           margin:0 0 6px;">{title}</h3>
                <p style="color:#3d4455;font-size:13px;margin:0;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:2rem;'></div>", unsafe_allow_html=True)

    # ── AI Banner ─────────────────────────────────────────────────────────
    st.markdown("""
    <div class="zpots-card-dark" style="padding:2rem 2.5rem;">
        <span class="ai-tag on-dark" style="background:rgba(207,252,0,0.1);">
            POWERED BY ZPOTS AI</span>
        <h2 style="color:white !important;font-family:'Space Grotesk';font-size:1.8rem;
                   font-weight:700;margin-top:0.8rem;">
            Experience Precision<br>with
            <span style="color:#cffc00;">Smart Booking</span>
        </h2>
        <ul style="color:rgba(255,255,255,0.85);font-size:14px;
                   margin-top:1rem;list-style:none;padding:0;">
            <li style="margin-bottom:8px;">⚡ Dynamic pricing based on real-time court demand</li>
            <li style="margin-bottom:8px;">🎯 AI-suggested partners matching your skill level</li>
            <li style="margin-bottom:8px;">📊 Smart predictions &amp; live availability tracking</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div style='height:2rem;'></div>", unsafe_allow_html=True)
