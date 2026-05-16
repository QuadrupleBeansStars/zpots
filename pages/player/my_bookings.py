"""My Bookings - Player's booking list."""
from datetime import date as date_cls
import streamlit as st
from components.css import inject_global_css
from components.nav import navigate, render_player_topbar
from components.cards import booking_card_player
from data.dummy_data import COURTS
from data.database import get_bookings_by_user

COURT_LOOKUP = {c["id"]: c for c in COURTS}


def _enrich(bk: dict) -> dict:
    court = COURT_LOOKUP.get(bk["court_id"], {})
    try:
        d = date_cls.fromisoformat(bk["date"])
        bk["date"]      = d.strftime("%a, %d %b")
        bk["date_full"] = d.strftime("%A, %B %d, %Y")
    except Exception:
        bk["date_full"] = bk.get("date", "")
    bk.setdefault("color",        court.get("color", "#1a3a2a"))
    bk.setdefault("sport",        court.get("sport", "Sport"))
    bk.setdefault("ai_verified",  False)
    bk.setdefault("team_members", [])
    bk.setdefault("qr_code",      bk["txn_id"])
    bk.setdefault("court_name",   bk.get("court_name", ""))
    bk.setdefault("court_number", "01")
    bk.setdefault("surface",      court.get("surface", ""))
    bk.setdefault("address",      court.get("address", court.get("location", "")))
    bk.setdefault("address_note", "")
    bk.setdefault("id",           bk["txn_id"])
    dur_hrs = bk.get("duration", 1)
    bk.setdefault("duration_min", dur_hrs * 60)
    try:
        sh = int(bk.get("time_start", "0:00").split(":")[0])
        bk.setdefault("time_end", f"{sh + dur_hrs:02d}:00")
    except Exception:
        pass
    return bk


def render():
    inject_global_css()
    render_player_topbar()

    player_id = st.session_state.get("user_id")
    if not player_id:
        navigate("player_login")
        return

    raw_bookings = get_bookings_by_user(player_id)
    bookings = [_enrich(dict(b)) for b in raw_bookings]

    user_name = st.session_state.get("user_name", "Player")
    st.markdown(f"""
    <h1 style="font-family:'Space Grotesk';font-size:2rem;font-weight:700;margin:0;">
        My Bookings</h1>
    <p style="color:#3d4455;font-size:13px;margin-top:2px;">
        Welcome back, {user_name}. Here are your upcoming and past sessions.</p>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="display:flex;gap:8px;margin:20px 0 16px;">
        <span class="chip chip-selected">All</span>
        <span class="chip chip-default">Upcoming</span>
        <span class="chip chip-default">Past</span>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["All Bookings", "Past"])

    with tab1:
        if not bookings:
            st.markdown("""
        <div style="text-align:center;padding:60px;background:#F2F9EE;border-radius:16px;">
            <div style="font-size:48px;">🎾</div>
            <h3 style="font-family:'Space Grotesk';font-size:20px;font-weight:600;margin-top:10px;">
                No bookings yet</h3>
            <p style="color:#3d4455;margin-top:6px;font-size:13px;">
                Start by searching for a court.</p>
        </div>
        """, unsafe_allow_html=True)
            if st.button("Find a Court", type="primary", key="empty_find_court"):
                navigate("player_search")
            return

        for i, bk in enumerate(bookings):
            booking_card_player(bk, key_prefix=f"bk_{i}")
            if st.button("Manage Booking", key=f"manage_{i}"):
                navigate("checkin_qr", selected_booking_id=bk["txn_id"])
            st.markdown("<div style='height:0.75rem;'></div>", unsafe_allow_html=True)

    with tab2:
        past = [b for b in bookings if b.get("status") in ("CONFIRMED", "COMPLETED")]
        if not past:
            st.markdown('<div style="text-align:center; padding:2rem; color:#3d4455;"><span style="font-size:2rem;">📋</span><p>No past bookings to show yet.</p></div>', unsafe_allow_html=True)
        else:
            for i, bk in enumerate(past):
                html = (
                    f'<div class="zpots-card">'
                    f'<div style="display:flex; align-items:center; gap:1rem;">'
                    f'<span style="font-size:2rem;">🎾</span>'
                    f'<div style="flex:1;">'
                    f'<div style="font-family:\'Inter\'; font-weight:600; font-size:16px;">{bk["court_name"]}</div>'
                    f'<div style="margin-top:6px;">'
                    f'<span style="font-size:13px; color:#3d4455;">📅 {bk["date"]}</span>'
                    f'<span style="font-size:13px; color:#3d4455; margin-left:12px;">🕐 {bk["time_start"]} - {bk["time_end"]}</span>'
                    f'</div>'
                    f'<div style="font-size:12px; color:#3d4455; margin-top:4px;">ID: {bk["txn_id"]}</div>'
                    f'</div>'
                    f'</div>'
                    f'</div>'
                )
                st.markdown(html, unsafe_allow_html=True)

    st.markdown("<div style='height:1.5rem;'></div>", unsafe_allow_html=True)

    snap_col, review_col = st.columns(2)
    with snap_col:
        total_sessions = len(bookings)
        total_hours = sum(b.get("duration", 1) for b in bookings)
        st.markdown(f"""
        <div class="zpots-card-lime" style="padding:1.5rem;">
            <div style="font-family:'Lexend'; font-size:10px; text-transform:uppercase; letter-spacing:0.1em; color:#1a2600; margin-bottom:12px;">Activity Snapshot</div>
            <div style="display:flex; justify-content:space-between; margin-bottom:12px;">
                <span style="font-size:13px; color:#1a2600;">Total Sessions Booked</span>
                <span style="font-family:'Space Grotesk'; font-weight:700; font-size:20px; color:#1a2600;">{total_sessions}</span>
            </div>
            <div style="display:flex; justify-content:space-between;">
                <span style="font-size:13px; color:#1a2600;">Total Hours Booked</span>
                <span style="font-family:'Space Grotesk'; font-weight:700; font-size:20px; color:#1a2600;">{total_hours}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with review_col:
        st.markdown("""
        <div class="zpots-card" style="display:flex; align-items:center; gap:1rem; cursor:pointer;">
            <span style="font-size:2rem;">🕐</span>
            <div>
                <div style="font-family:'Inter'; font-weight:600; font-size:16px;">Your Booking History</div>
                <div style="font-size:13px; color:#3d4455;">All your sessions across all courts.</div>
            </div>
            <span style="font-size:18px; color:#3d4455;">→</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)
    if st.button("⭐ Leave Feedback for Last Session", key="leave_feedback_btn", width='stretch'):
        navigate("leave_feedback")
