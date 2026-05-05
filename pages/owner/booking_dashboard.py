"""Owner Booking Dashboard - Revenue and booking management."""
from datetime import date as date_cls, datetime
import streamlit as st
from components.css import inject_global_css, inject_owner_sidebar_css
from components.nav import navigate, render_owner_sidebar
from data.dummy_data import OWNER_BOOKINGS, COURTS
from data.database import get_all_bookings
from utils.ml_inference import predict_noshow_risk

COURT_LOOKUP = {c["id"]: c for c in COURTS}


def render():
    inject_global_css()
    inject_owner_sidebar_css()
    render_owner_sidebar()

    st.markdown("# Bookings")

    # Revenue banner
    st.markdown("""
    <div class="revenue-banner">
        <div style="display:flex; justify-content:space-between; align-items:flex-start;">
            <div>
                <div style="font-family:'Lexend'; font-size:10px; text-transform:uppercase; letter-spacing:0.1em; color:rgba(255,255,255,0.7);">TOTAL REVENUE TODAY</div>
                <div style="font-family:'Space Grotesk'; font-weight:700; font-size:3rem; color:white; line-height:1.1;">$4,280.50</div>
                <div style="font-size:13px; color:rgba(255,255,255,0.8); margin-top:4px;">📈 +12.5% from yesterday</div>
            </div>
            <div>
                <div style="font-family:'Lexend'; font-size:9px; text-transform:uppercase; letter-spacing:0.1em; color:rgba(255,255,255,0.6);">ACTIVE NOW</div>
                <div style="font-family:'Space Grotesk'; font-weight:600; font-size:1.3rem; color:white; font-style:italic;">Upcoming</div>
            </div>
        </div>
        <div style="display:flex; gap:1rem; margin-top:1.5rem;">
            <div style="background:rgba(255,255,255,0.15); border-radius:12px; padding:8px 16px;">
                <div style="font-size:10px; color:rgba(255,255,255,0.6);">MAIN ARENA</div>
                <div style="font-family:'Space Grotesk'; font-weight:700; color:white;">$1,240</div>
            </div>
            <div style="background:rgba(255,255,255,0.15); border-radius:12px; padding:8px 16px;">
                <div style="font-size:10px; color:rgba(255,255,255,0.6);">PADEL POD 2</div>
                <div style="font-family:'Space Grotesk'; font-weight:700; color:white;">$890</div>
            </div>
            <div style="background:rgba(207,252,0,0.3); border-radius:12px; padding:8px 16px;">
                <div style="font-size:10px; color:rgba(255,255,255,0.6);">INDOOR TURF</div>
                <div style="font-family:'Space Grotesk'; font-weight:700; color:white;">$2,150</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)

    # Upcoming sidebar
    st.markdown("""
    <div class="zpots-card" style="margin-bottom:1rem;">
        <div style="font-family:'Inter'; font-weight:600; margin-bottom:8px;">
            <span style="color:#cffc00; font-size:10px;">●</span> Semi-Pro Tournament
        </div>
        <div style="font-size:12px; color:#3d4455;">14:00 - 16:30 • Court A</div>
        <hr>
        <div style="font-family:'Inter'; font-weight:600; margin-bottom:4px;">Junior Training</div>
        <div style="font-size:12px; color:#3d4455;">12:30 - 14:00 • Pitch 4</div>
        <hr>
        <div style="font-family:'Inter'; font-weight:600; margin-bottom:4px;">Corporate Mix</div>
        <div style="font-size:12px; color:#3d4455;">17:30 - 19:00 • Club Court</div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Today", "This Week", "Calendar"])

    with tab1:
        fcol1, fcol2 = st.columns(2)
        with fcol1:
            st.selectbox("Venue", ["All Venues", "Main Arena", "Padel Pod 2", "Indoor Turf"], key="venue_filter")
        with fcol2:
            st.selectbox("Sort", ["Time Ascending", "Time Descending", "Status"], key="sort_filter")

        st.markdown("""
        <div style="display:grid; grid-template-columns: 2fr 2fr 1fr 1fr 0.5fr; gap:0; padding:12px 16px; font-family:'Lexend'; font-size:10px; text-transform:uppercase; letter-spacing:0.08em; color:#3d4455;">
            <div>CUSTOMER</div><div>SESSION INFO</div><div>STATUS</div><div>RISK</div><div>ACTION</div>
        </div>
        """, unsafe_allow_html=True)

        # Build real bookings from DB
        db_rows = get_all_bookings()
        real_bookings = []
        for bk in db_rows:
            court = COURT_LOOKUP.get(bk["court_id"], {})
            sport = court.get("sport", "Sport")
            dur = bk.get("duration", 1)
            try:
                d = date_cls.fromisoformat(bk["date"])
                date_label = d.strftime("%a %d %b")
            except Exception:
                date_label = bk.get("date", "")
            real_bookings.append({
                "customer":     bk["player_name"],
                "member_id":    f"#{bk['txn_id']}",
                "court":        bk["court_name"],
                "sport":        sport,
                "time":         f"{bk['time_start']} - {bk['time_end']} ({dur * 60} min) • {date_label}",
                "status":       bk["status"],
                "avatar_color": "#2E6B00",
            })

        all_bookings = real_bookings + OWNER_BOOKINGS

        TIER_TO_CSS = {"Low": "status-active", "Medium": "status-warning", "High": "status-cancelled"}

        for booking in all_bookings:
            status_class = f"status-{booking['status'].lower()}"
            sport = booking.get("sport", "Badminton")
            time_str = booking.get("time", "")
            try:
                hour = int(time_str.split(":")[0][-2:])
            except Exception:
                hour = 18
            today = datetime.now()
            feat = {
                "sport": sport,
                "district": "Sukhumvit",
                "day_of_week": today.weekday(),
                "hour": hour,
                "is_weekend": today.weekday() >= 5,
                "is_holiday": False,
                "weather": "sunny",
                "price": 500,
                "lead_time_days": 5,
                "is_repeat_customer": booking.get("status", "").upper() == "COMPLETED",
            }
            tier, _prob = predict_noshow_risk(feat)
            risk_class = TIER_TO_CSS[tier]

            st.markdown(f"""
            <div class="zpots-card" style="display:grid; grid-template-columns: 2fr 2fr 1fr 1fr 0.5fr; gap:0; align-items:center; margin-bottom:8px; padding:12px 16px;">
                <div style="display:flex; align-items:center; gap:10px;">
                    <div style="width:36px; height:36px; border-radius:50%; background:{booking['avatar_color']}; color:white; display:flex; align-items:center; justify-content:center; font-size:14px; font-weight:600;">{booking['customer'][0]}</div>
                    <div>
                        <div style="font-family:'Inter'; font-weight:600; font-size:14px;">{booking['customer']}</div>
                        <div style="font-size:11px; color:#3d4455;">Member ID: {booking['member_id']}</div>
                    </div>
                </div>
                <div>
                    <div style="font-size:13px;">🏟 {booking['court']} • {booking['sport']}</div>
                    <div style="font-size:12px; color:#3d4455;">🕐 {booking['time']}</div>
                </div>
                <div><span class="status-badge {status_class}">{booking['status']}</span></div>
                <div><span class="status-badge {risk_class}">{tier}</span></div>
                <div style="text-align:center; cursor:pointer; font-size:18px;">⋮</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f'<div style="font-size:12px; color:#3d4455; margin-top:1rem;">SHOWING {len(all_bookings)} BOOKINGS ({len(real_bookings)} real + {len(OWNER_BOOKINGS)} historical demo)</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<p style="color:#3d4455;">Weekly booking overview coming soon.</p>', unsafe_allow_html=True)
    with tab3:
        st.markdown('<p style="color:#3d4455;">Calendar view coming soon.</p>', unsafe_allow_html=True)
