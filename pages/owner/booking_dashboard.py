"""Owner Booking Dashboard - Revenue and booking management."""
import streamlit as st
from components.css import inject_global_css, inject_owner_sidebar_css
from components.nav import navigate, render_owner_sidebar
from data.dummy_data import OWNER_BOOKINGS


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
        <div style="font-size:12px; color:#535b71;">14:00 - 16:30 • Court A</div>
        <hr>
        <div style="font-family:'Inter'; font-weight:600; margin-bottom:4px;">Junior Training</div>
        <div style="font-size:12px; color:#535b71;">12:30 - 14:00 • Pitch 4</div>
        <hr>
        <div style="font-family:'Inter'; font-weight:600; margin-bottom:4px;">Corporate Mix</div>
        <div style="font-size:12px; color:#535b71;">17:30 - 19:00 • Club Court</div>
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
        <div style="display:grid; grid-template-columns: 2fr 2fr 1fr 0.5fr; gap:0; padding:12px 16px; font-family:'Lexend'; font-size:10px; text-transform:uppercase; letter-spacing:0.08em; color:#535b71;">
            <div>CUSTOMER</div><div>SESSION INFO</div><div>STATUS</div><div>ACTION</div>
        </div>
        """, unsafe_allow_html=True)

        for booking in OWNER_BOOKINGS:
            status_class = f"status-{booking['status'].lower()}"
            st.markdown(f"""
            <div class="zpots-card" style="display:grid; grid-template-columns: 2fr 2fr 1fr 0.5fr; gap:0; align-items:center; margin-bottom:8px; padding:12px 16px;">
                <div style="display:flex; align-items:center; gap:10px;">
                    <div style="width:36px; height:36px; border-radius:50%; background:{booking['avatar_color']}; color:white; display:flex; align-items:center; justify-content:center; font-size:14px; font-weight:600;">{booking['customer'][0]}</div>
                    <div>
                        <div style="font-family:'Inter'; font-weight:600; font-size:14px;">{booking['customer']}</div>
                        <div style="font-size:11px; color:#535b71;">Member ID: {booking['member_id']}</div>
                    </div>
                </div>
                <div>
                    <div style="font-size:13px;">🏟 {booking['court']} • {booking['sport']}</div>
                    <div style="font-size:12px; color:#535b71;">🕐 {booking['time']}</div>
                </div>
                <div><span class="status-badge {status_class}">{booking['status']}</span></div>
                <div style="text-align:center; cursor:pointer; font-size:18px;">⋮</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div style="font-size:12px; color:#535b71; margin-top:1rem;">SHOWING 4 OF 128 BOOKINGS</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<p style="color:#535b71;">Weekly booking overview coming soon.</p>', unsafe_allow_html=True)
    with tab3:
        st.markdown('<p style="color:#535b71;">Calendar view coming soon.</p>', unsafe_allow_html=True)
