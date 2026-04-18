"""My Bookings - Player's booking list."""
import streamlit as st
from components.css import inject_global_css
from components.nav import navigate, render_player_topbar
from components.cards import booking_card_player
from data.dummy_data import PLAYER_BOOKINGS


def render():
    inject_global_css()
    render_player_topbar()

    st.markdown("""
    <h1 style="font-family:'Space Grotesk';font-size:2rem;font-weight:700;margin:0;">
        My Bookings</h1>
    <p style="color:#3d4455;font-size:13px;margin-top:2px;">
        Upcoming games and past sessions.</p>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="display:flex;gap:8px;margin:20px 0 16px;">
        <span class="chip chip-selected">Upcoming</span>
        <span class="chip chip-default">Past</span>
        <span class="chip chip-default">Cancelled</span>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Upcoming", "Past"])

    with tab1:
        if not PLAYER_BOOKINGS:
            st.markdown("""
        <div style="text-align:center;padding:60px;background:#F2F9EE;border-radius:16px;">
            <div style="font-size:48px;">🎾</div>
            <h3 style="font-family:'Space Grotesk';font-size:20px;font-weight:600;margin-top:10px;">
                No upcoming bookings</h3>
            <p style="color:#3d4455;margin-top:6px;font-size:13px;">
                Start by searching for a court.</p>
        </div>
        """, unsafe_allow_html=True)
            if st.button("Find a Court", type="primary", key="empty_find_court"):
                navigate("player_search")
            return

        booking_card_player(PLAYER_BOOKINGS[0], key_prefix="upcoming_0")
        st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)

        b = PLAYER_BOOKINGS[1]
        st.markdown(f"""
        <div class="zpots-card">
            <div style="display:flex; align-items:center; gap:1rem;">
                <span style="font-size:2rem;">🎾</span>
                <div style="flex:1;">
                    <div style="font-family:'Inter'; font-weight:600; font-size:16px;">{b['court_name']}</div>
                    <div style="font-family:'Lexend'; font-size:10px; text-transform:uppercase; color:#3d4455;">PREMIUM COURT • INDOOR</div>
                    <div style="margin-top:6px;">
                        <span style="font-size:13px; color:#3d4455;">📅 {b['date']}</span>
                        <span style="font-size:13px; color:#3d4455; margin-left:12px;">🕐 {b['time_start']} - {b['time_end']}</span>
                    </div>
                    <div style="font-size:12px; color:#3d4455; margin-top:4px;">📍 {b['address']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Manage Booking", key="manage_booking_2"):
            navigate("checkin_qr", selected_booking_id=b["id"])

    with tab2:
        st.markdown('<div style="text-align:center; padding:2rem; color:#3d4455;"><span style="font-size:2rem;">📋</span><p>No past bookings to show yet.</p></div>', unsafe_allow_html=True)

    st.markdown("<div style='height:1.5rem;'></div>", unsafe_allow_html=True)

    snap_col, review_col = st.columns(2)
    with snap_col:
        st.markdown("""
        <div class="zpots-card-lime" style="padding:1.5rem;">
            <div style="font-family:'Lexend'; font-size:10px; text-transform:uppercase; letter-spacing:0.1em; color:#1a2600; margin-bottom:12px;">Activity Snapshot</div>
            <div style="display:flex; justify-content:space-between; margin-bottom:12px;">
                <span style="font-size:13px; color:#1a2600;">Total Hours This Month</span>
                <span style="font-family:'Space Grotesk'; font-weight:700; font-size:20px; color:#1a2600;">12.5</span>
            </div>
            <div style="display:flex; justify-content:space-between;">
                <span style="font-size:13px; color:#1a2600;">Credits Remaining</span>
                <span style="font-family:'Space Grotesk'; font-weight:700; font-size:20px; color:#1a2600;">450</span>
            </div>
            <div style="margin-top:12px; height:4px; background:rgba(0,0,0,0.1); border-radius:2px;">
                <div style="height:100%; width:65%; background:#4b5e00; border-radius:2px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with review_col:
        st.markdown("""
        <div class="zpots-card" style="display:flex; align-items:center; gap:1rem; cursor:pointer;">
            <span style="font-size:2rem;">🕐</span>
            <div>
                <div style="font-family:'Inter'; font-weight:600; font-size:16px;">Review 24 Past Sessions</div>
                <div style="font-size:13px; color:#3d4455;">Analyze your performance and recurring slot patterns.</div>
            </div>
            <span style="font-size:18px; color:#3d4455;">→</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)
    if st.button("⭐ Leave Feedback for Last Session", key="leave_feedback_btn", width='stretch'):
        navigate("leave_feedback")
