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

    hcol1, hcol2 = st.columns([3, 1], vertical_alignment="bottom")
    with hcol1:
        st.title("Venue Performance")
        st.caption("Real-time metrics for your Bangkok sports facilities.")
    with hcol2:
        if st.button("Add Court", type="primary", icon=":material/add_circle:", key="dash_add_court"):
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

    st.space("small")

    chart_col, ai_col = st.columns([1.5, 1], gap="medium")

    with chart_col:
        st.markdown('<div class="zpots-card"><h3 style="font-size:1rem; margin:0;">Utilization Trends</h3></div>', unsafe_allow_html=True)
        st.radio("Period", ["Daily", "Weekly", "Monthly"], horizontal=True, key="util_period", label_visibility="collapsed")
        st.plotly_chart(utilization_bar_chart(WEEKLY_UTILIZATION), use_container_width=True, config={"displayModeBar": False})

    with ai_col:
        st.markdown("""
<div class="zpots-card-lime" style="padding:20px;margin-bottom:10px;">
    <div style="display:flex;align-items:center;gap:6px;margin-bottom:6px;">
        <span style="font-size:14px;">⚡</span>
        <span style="font-weight:700;font-size:14px;color:#1a2600;">
            AI Revenue Optimizer</span>
    </div>
    <p style="font-size:13px;color:#1a2600;line-height:1.5;">
        Demand for <strong>Friday Evening</strong> is up by <strong>30%</strong>.
        Consider raising prices for 18:00–21:00 slots to maximize revenue.</p>
    <div style="font-size:12px;color:#1a2600;margin-top:10px;">
        ● Apply Dynamic Pricing for this weekend</div>
</div>
""", unsafe_allow_html=True)
        if st.button("Apply Now", type="primary", key="apply_ai", width='stretch'):
            st.toast("AI pricing applied!")

    st.space("small")

    book_col, venue_col = st.columns([1.5, 1], gap="medium")

    with book_col:
        st.markdown("""
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem;">
            <h3 style="font-size:1rem; margin:0;">Today's Bookings</h3>
        </div>
        """, unsafe_allow_html=True)

        for booking in TODAYS_BOOKINGS:
            status_cls = (
                "status-confirmed" if booking["status"] == "CONFIRMED"
                else "status-progress" if booking["status"] == "IN PROGRESS"
                else "status-completed"
            )
            st.markdown(f"""
<div class="zpots-card" style="display:flex;align-items:center;gap:18px;
             margin-bottom:8px;padding:16px 20px;">
    <div>
        <span class="display" style="font-size:18px;">{booking['time']}</span>
        <div class="eyebrow" style="font-size:9px;">{booking['type']}</div>
    </div>
    <div style="flex:1;">
        <div style="font-weight:600;font-size:14px;">{booking['title']}</div>
        <div style="font-size:12px;color:#3d4455;">
            Customer: {booking['customer']} · {booking['venue']}</div>
    </div>
    <span class="status-badge {status_cls}">{booking['status']}</span>
</div>
""", unsafe_allow_html=True)

        if st.button("View All Bookings →", key="view_all_bookings"):
            navigate("booking_dashboard")

    with venue_col:
        st.markdown("""
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem;">
            <h3 style="font-size:1rem; margin:0;">Manage Venues</h3>
            <span style="font-family:'Lexend'; font-size:10px; text-transform:uppercase; letter-spacing:0.1em; color:#3d4455;">3 LOCATIONS</span>
        </div>
        """, unsafe_allow_html=True)

        for venue in OWNER_VENUES:
            venue_card_owner(venue, key_prefix="dash_venue")
            st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)
