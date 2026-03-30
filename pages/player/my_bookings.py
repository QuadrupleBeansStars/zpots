"""My Bookings - Player's booking list."""
import streamlit as st
from components.css import inject_global_css
from components.nav import navigate, render_player_topbar
from components.cards import booking_card_player
from data.dummy_data import PLAYER_BOOKINGS


def render():
    inject_global_css()
    render_player_topbar()

    st.markdown('<div style="font-family:\'Lexend\'; font-size:10px; text-transform:uppercase; letter-spacing:0.1em; color:#535b71;">YOUR ACTIVITY</div>', unsafe_allow_html=True)
    st.markdown("# Bookings")

    tab1, tab2 = st.tabs(["Upcoming", "Past"])

    with tab1:
        booking_card_player(PLAYER_BOOKINGS[0], key_prefix="upcoming_0")
        st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)

        b = PLAYER_BOOKINGS[1]
        st.markdown(f"""
        <div class="zpots-card">
            <div style="display:flex; align-items:center; gap:1rem;">
                <span style="font-size:2rem;">🎾</span>
                <div style="flex:1;">
                    <div style="font-family:'Inter'; font-weight:600; font-size:16px;">{b['court_name']}</div>
                    <div style="font-family:'Lexend'; font-size:10px; text-transform:uppercase; color:#535b71;">PREMIUM COURT • INDOOR</div>
                    <div style="margin-top:6px;">
                        <span style="font-size:13px; color:#535b71;">📅 {b['date']}</span>
                        <span style="font-size:13px; color:#535b71; margin-left:12px;">🕐 {b['time_start']} - {b['time_end']}</span>
                    </div>
                    <div style="font-size:12px; color:#535b71; margin-top:4px;">📍 {b['address']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Manage Booking", key="manage_booking_2"):
            navigate("checkin_qr", selected_booking_id=b["id"])

    with tab2:
        st.markdown('<div style="text-align:center; padding:2rem; color:#535b71;"><span style="font-size:2rem;">📋</span><p>No past bookings to show yet.</p></div>', unsafe_allow_html=True)

    st.markdown("<div style='height:1.5rem;'></div>", unsafe_allow_html=True)

    snap_col, review_col = st.columns(2)
    with snap_col:
        st.markdown("""
        <div class="zpots-card-lime" style="padding:1.5rem;">
            <div style="font-family:'Lexend'; font-size:10px; text-transform:uppercase; letter-spacing:0.1em; color:#4b5e00; margin-bottom:12px;">Activity Snapshot</div>
            <div style="display:flex; justify-content:space-between; margin-bottom:12px;">
                <span style="font-size:13px; color:#4b5e00;">Total Hours This Month</span>
                <span style="font-family:'Space Grotesk'; font-weight:700; font-size:20px; color:#4b5e00;">12.5</span>
            </div>
            <div style="display:flex; justify-content:space-between;">
                <span style="font-size:13px; color:#4b5e00;">Credits Remaining</span>
                <span style="font-family:'Space Grotesk'; font-weight:700; font-size:20px; color:#4b5e00;">450</span>
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
                <div style="font-size:13px; color:#535b71;">Analyze your performance and recurring slot patterns.</div>
            </div>
            <span style="font-size:18px; color:#535b71;">→</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)
    if st.button("⭐ Leave Feedback for Last Session", key="leave_feedback_btn", use_container_width=True):
        navigate("leave_feedback")
