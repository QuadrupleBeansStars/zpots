"""Manage Courts - Court listing and management."""
import streamlit as st
from components.css import inject_global_css, inject_owner_sidebar_css
from components.nav import navigate, render_owner_sidebar
from data.dummy_data import COURTS
from components.charts import mini_bar_chart


def render():
    inject_global_css()
    inject_owner_sidebar_css()
    render_owner_sidebar()

    st.markdown("""
    <h1 style="font-size:2rem; margin-bottom:0;">Manage Courts</h1>
    <p style="color:#3d4455; font-size:14px;">Real-time performance metrics and availability control for your elite sports facilities.</p>
    """, unsafe_allow_html=True)

    view = st.radio("View", ["GRID", "LIST"], horizontal=True, key="courts_view",
                    label_visibility="collapsed")

    st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)

    court_col, insight_col = st.columns([1.5, 1])

    SPORT_ICON = {"Badminton": "🏸", "Football": "⚽", "Padel": "🎾",
                  "Basketball": "🏀", "Tennis": "🎾"}

    with court_col:
        if view == "GRID":
            for court in COURTS:
                icon = SPORT_ICON.get(court["sport"], "🏟")
                st.markdown(f"""
<div class="zpots-card" style="padding:0; overflow:hidden; margin-bottom:1rem;">
    <div class="court-image" style="background:linear-gradient(135deg, {court['color']}, {court['color']}cc); height:160px; position:relative; display:flex; align-items:center; justify-content:center;">
        <span style="font-size:3rem;">{icon}</span>
        <span class="status-badge status-active" style="position:absolute; top:12px; left:12px; background:rgba(207,252,0,0.9);">● {court['status']}</span>
    </div>
    <div style="padding:1.2rem;">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <div>
                <div style="font-family:'Inter'; font-weight:700; font-size:18px;">{court['name']}</div>
                <div style="font-size:13px; color:#3d4455;">📍 {court['district']}, Bangkok</div>
            </div>
        </div>
        <div style="display:flex; gap:2rem; margin-top:12px;">
            <div>
                <div style="font-family:'Lexend'; font-size:9px; text-transform:uppercase; letter-spacing:0.1em; color:#3d4455;">UTILIZATION</div>
                <div style="font-family:'Space Grotesk'; font-weight:700; font-size:1.3rem;">{court['utilization']}%</div>
            </div>
            <div>
                <div style="font-family:'Lexend'; font-size:9px; text-transform:uppercase; letter-spacing:0.1em; color:#3d4455;">PEAK HOURS</div>
                <div style="font-family:'Space Grotesk'; font-weight:700; font-size:1.3rem;">{court['peak_hours']}</div>
            </div>
            <div>
                <div style="font-family:'Lexend'; font-size:9px; text-transform:uppercase; letter-spacing:0.1em; color:#3d4455;">AI EFFICIENCY</div>
                <div style="font-family:'Space Grotesk'; font-weight:700; font-size:1.3rem; font-style:italic;">{court['ai_efficiency']}</div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
                if st.button("Edit Court", key=f"edit_court_{court['id']}", width='stretch'):
                    navigate("add_edit_court", editing_court_id=court["id"])
        else:  # LIST view — compact one-row-per-court
            st.markdown("""
<div class="zpots-card" style="padding:0; overflow:hidden;">
    <div style="display:grid; grid-template-columns:48px 2fr 1fr 1fr 1fr 100px;
                gap:12px; padding:12px 16px; background:#f6f6ff;
                font-family:'Lexend'; font-size:10px; text-transform:uppercase;
                letter-spacing:0.08em; color:#3d4455;">
        <div></div><div>Court</div><div>District</div><div>Utilization</div>
        <div>Peak hours</div><div></div>
    </div>
""", unsafe_allow_html=True)
            for court in COURTS:
                icon = SPORT_ICON.get(court["sport"], "🏟")
                st.markdown(f"""
<div style="display:grid; grid-template-columns:48px 2fr 1fr 1fr 1fr 100px;
            gap:12px; padding:14px 16px; border-bottom:1px solid #eef0ff;
            align-items:center; background:white;">
    <div style="width:36px; height:36px; border-radius:8px;
                background:linear-gradient(135deg, {court['color']}, {court['color']}cc);
                display:flex; align-items:center; justify-content:center;
                font-size:18px;">{icon}</div>
    <div>
        <div style="font-weight:600; font-size:14px;">{court['name']}</div>
        <div style="font-size:11px; color:#3d4455;">{court['sport']}</div>
    </div>
    <div style="font-size:13px;">{court['district']}</div>
    <div style="font-family:'Space Grotesk'; font-weight:700;">{court['utilization']}%</div>
    <div style="font-size:13px;">{court['peak_hours']}</div>
    <div></div>
</div>
""", unsafe_allow_html=True)
                # Inline Edit per row (Streamlit can't embed buttons in markdown HTML).
                if st.button("Edit", key=f"list_edit_{court['id']}"):
                    navigate("add_edit_court", editing_court_id=court["id"])
            st.markdown("</div>", unsafe_allow_html=True)

    with insight_col:
        st.markdown("""
        <div class="zpots-card-surface" style="padding:1.5rem;">
            <span style="font-size:1.5rem;">📈</span>
            <h3 style="font-size:1.1rem; margin-top:8px;">Monthly Performance Insight</h3>
            <p style="font-size:13px; color:#3d4455; margin-top:8px;">Your Bangkok venue is outperforming the regional average by <strong>24%</strong> this month. Consider dynamic pricing for weekend slots.</p>
        </div>
        """, unsafe_allow_html=True)

        st.plotly_chart(mini_bar_chart([65, 72, 58, 80, 91, 88, 45]), width='stretch', config={"displayModeBar": False})

        if st.button("View Full Analytics →", key="view_analytics"):
            navigate("ai_insights")

        st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)

        st.markdown("""
        <div class="zpots-card-surface" style="text-align:center; padding:2rem;">
            <div style="width:48px; height:48px; border-radius:50%; background:#e2e7ff; display:flex; align-items:center; justify-content:center; font-size:24px; margin:0 auto 12px auto;">+</div>
            <h3 style="font-size:1rem;">Register a New Venue</h3>
            <p style="font-size:13px; color:#3d4455;">Expand your portfolio. Add a badminton court, football pitch, or padel arena in seconds.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Register Venue", type="primary", key="register_venue", width='stretch'):
            navigate("add_edit_court", editing_court_id=None)
