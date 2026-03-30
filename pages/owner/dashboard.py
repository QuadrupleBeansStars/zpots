"""Owner Dashboard - Venue Performance."""
import streamlit as st
from components.css import inject_global_css, inject_owner_sidebar_css
from components.nav import navigate, render_owner_sidebar
from components.cards import kpi_card, venue_card_owner
from components.charts import utilization_bar_chart
from data.dummy_data import WEEKLY_UTILIZATION, OWNER_VENUES, TODAYS_BOOKINGS


def render():
    inject_global_css()
    inject_owner_sidebar_css()
    render_owner_sidebar()

    hcol1, hcol2 = st.columns([3, 1])
    with hcol1:
        st.markdown("""
        <h1 style="font-size:2rem; margin-bottom:0;">Venue Performance</h1>
        <p style="color:#535b71; font-size:14px;">Real-time metrics for your Bangkok sports facilities.</p>
        """, unsafe_allow_html=True)
    with hcol2:
        if st.button("➕ Add Court", type="primary", key="dash_add_court"):
            navigate("add_edit_court", editing_court_id=None)

    kpi_cols = st.columns(4)
    with kpi_cols[0]:
        kpi_card("TOTAL BOOKINGS", "128", delta="↗ +12%", icon="📅")
    with kpi_cols[1]:
        kpi_card("TOTAL REVENUE", "64,500 THB", delta="October 2024", icon="💰")
    with kpi_cols[2]:
        kpi_card("AVG UTILIZATION", "72%", icon="📊")
    with kpi_cols[3]:
        kpi_card("TOP RATED COURT", "Court 3", delta="4.8 ⭐ (142 reviews)", icon="⭐")

    st.markdown("<div style='height:1.5rem;'></div>", unsafe_allow_html=True)

    chart_col, ai_col = st.columns([1.5, 1])

    with chart_col:
        st.markdown('<div class="zpots-card"><h3 style="font-size:1rem; margin:0;">Utilization Trends</h3></div>', unsafe_allow_html=True)
        st.radio("Period", ["Daily", "Weekly", "Monthly"], horizontal=True, key="util_period", label_visibility="collapsed")
        st.plotly_chart(utilization_bar_chart(WEEKLY_UTILIZATION), use_container_width=True, config={"displayModeBar": False})

    with ai_col:
        st.markdown("""
        <div class="zpots-card-lime" style="padding:1.5rem;">
            <div style="display:flex; align-items:center; gap:6px; margin-bottom:8px;">
                <span style="font-size:14px;">⚡</span>
                <span style="font-family:'Inter'; font-weight:700; font-size:14px; color:#4b5e00;">AI Revenue Optimizer</span>
            </div>
            <p style="font-size:13px; color:#4b5e00; margin-bottom:12px;">Demand for <strong>Friday Evening</strong> is up by <strong>30%</strong>. Consider raising prices for 18:00-21:00 slots to maximize revenue.</p>
            <div style="display:flex; align-items:center; gap:6px;">
                <span style="color:#4b5e00; font-size:12px;">●</span>
                <span style="font-size:12px; color:#4b5e00;">Apply Dynamic Pricing for this weekend</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Apply Now", type="primary", key="apply_ai", use_container_width=True):
            st.toast("AI pricing applied!")

    st.markdown("<div style='height:1.5rem;'></div>", unsafe_allow_html=True)

    book_col, venue_col = st.columns([1.5, 1])

    with book_col:
        st.markdown("""
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem;">
            <h3 style="font-size:1rem; margin:0;">Today's Bookings</h3>
        </div>
        """, unsafe_allow_html=True)

        for booking in TODAYS_BOOKINGS:
            status_color = "#cffc00" if booking["status"] == "CONFIRMED" else "#e2e7ff" if booking["status"] == "IN PROGRESS" else "#f6f6ff"
            st.markdown(f"""
            <div class="zpots-card" style="display:flex; align-items:center; gap:1rem; margin-bottom:8px; padding:1rem;">
                <div>
                    <span style="font-family:'Space Grotesk'; font-weight:700; font-size:18px;">{booking['time']}</span>
                    <div style="font-family:'Lexend'; font-size:9px; color:#535b71;">{booking['type']}</div>
                </div>
                <div style="flex:1;">
                    <div style="font-family:'Inter'; font-weight:600; font-size:14px;">{booking['title']}</div>
                    <div style="font-size:12px; color:#535b71;">Customer: {booking['customer']} • {booking['venue']}</div>
                </div>
                <span class="status-badge" style="background:{status_color}; padding:4px 12px; border-radius:999px; font-size:10px; font-weight:600;">{booking['status']}</span>
            </div>
            """, unsafe_allow_html=True)

        if st.button("View All Bookings →", key="view_all_bookings"):
            navigate("booking_dashboard")

    with venue_col:
        st.markdown("""
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem;">
            <h3 style="font-size:1rem; margin:0;">Manage Venues</h3>
            <span style="font-family:'Lexend'; font-size:10px; text-transform:uppercase; letter-spacing:0.1em; color:#535b71;">3 LOCATIONS</span>
        </div>
        """, unsafe_allow_html=True)

        for venue in OWNER_VENUES:
            venue_card_owner(venue, key_prefix="dash_venue")
            st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)
