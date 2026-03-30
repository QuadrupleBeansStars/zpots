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
    <p style="color:#535b71; font-size:14px;">Real-time performance metrics and availability control for your elite sports facilities.</p>
    """, unsafe_allow_html=True)

    st.radio("View", ["GRID", "LIST"], horizontal=True, key="courts_view", label_visibility="collapsed")

    st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)

    court_col, insight_col = st.columns([1.5, 1])

    with court_col:
        court = COURTS[0]
        st.markdown(f"""
        <div class="zpots-card" style="padding:0; overflow:hidden; margin-bottom:1rem;">
            <div class="court-image" style="background:linear-gradient(135deg, {court['color']}, {court['color']}cc); height:200px; position:relative;">
                <span style="font-size:3rem;">🏸</span>
                <span class="status-badge status-active" style="position:absolute; top:12px; left:12px; background:rgba(207,252,0,0.9);">● ACTIVE</span>
            </div>
            <div style="padding:1.2rem;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <div style="font-family:'Inter'; font-weight:700; font-size:18px;">{court['name']}</div>
                        <div style="font-size:13px; color:#535b71;">📍 {court['district']}, Bangkok</div>
                    </div>
                    <span style="font-size:18px; cursor:pointer;">✏️</span>
                </div>
                <div style="display:flex; gap:2rem; margin-top:12px;">
                    <div>
                        <div style="font-family:'Lexend'; font-size:9px; text-transform:uppercase; letter-spacing:0.1em; color:#535b71;">UTILIZATION</div>
                        <div style="font-family:'Space Grotesk'; font-weight:700; font-size:1.3rem;">{court['utilization']}%</div>
                    </div>
                    <div>
                        <div style="font-family:'Lexend'; font-size:9px; text-transform:uppercase; letter-spacing:0.1em; color:#535b71;">PEAK HOURS</div>
                        <div style="font-family:'Space Grotesk'; font-weight:700; font-size:1.3rem;">{court['peak_hours']}</div>
                    </div>
                    <div>
                        <div style="font-family:'Lexend'; font-size:9px; text-transform:uppercase; letter-spacing:0.1em; color:#535b71;">AI EFFICIENCY</div>
                        <div style="font-family:'Space Grotesk'; font-weight:700; font-size:1.3rem; font-style:italic;">{court['ai_efficiency']}</div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Edit Court", key="edit_court_1", use_container_width=True):
            navigate("add_edit_court", editing_court_id=court["id"])

        st.markdown("""
        <div class="zpots-card" style="padding:0; overflow:hidden; margin-top:1rem;">
            <div class="court-image" style="background:linear-gradient(135deg, #2a2a2a, #3a3a3a); height:120px; position:relative;">
                <span style="font-size:2rem;">🏗</span>
                <span class="status-badge status-maintenance" style="position:absolute; top:12px; left:12px; background:rgba(255,165,0,0.9); color:white;">MAINTENANCE</span>
            </div>
            <div style="padding:1rem;">
                <div style="font-family:'Inter'; font-weight:600; font-size:16px;">Ari Sports Center</div>
                <div style="font-size:12px; color:#535b71;">Status: Re-flooring in progress</div>
                <div style="display:flex; justify-content:space-between; margin-top:8px;">
                    <span style="font-size:12px; color:#535b71;">Estimated Completion</span>
                    <span style="font-family:'Inter'; font-weight:600;">Oct 24, 2023</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.button("Update Timeline", key="update_timeline")

    with insight_col:
        st.markdown("""
        <div class="zpots-card-surface" style="padding:1.5rem;">
            <span style="font-size:1.5rem;">📈</span>
            <h3 style="font-size:1.1rem; margin-top:8px;">Monthly Performance Insight</h3>
            <p style="font-size:13px; color:#535b71; margin-top:8px;">Your Bangkok venue is outperforming the regional average by <strong>24%</strong> this month. Consider dynamic pricing for weekend slots.</p>
        </div>
        """, unsafe_allow_html=True)

        st.plotly_chart(mini_bar_chart([65, 72, 58, 80, 91, 88, 45]), use_container_width=True, config={"displayModeBar": False})

        if st.button("View Full Analytics →", key="view_analytics"):
            navigate("ai_insights")

        st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)

        st.markdown("""
        <div class="zpots-card-surface" style="text-align:center; padding:2rem;">
            <div style="width:48px; height:48px; border-radius:50%; background:#e2e7ff; display:flex; align-items:center; justify-content:center; font-size:24px; margin:0 auto 12px auto;">+</div>
            <h3 style="font-size:1rem;">Register a New Venue</h3>
            <p style="font-size:13px; color:#535b71;">Expand your portfolio. Add a badminton court, football pitch, or padel arena in seconds.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Register Venue", type="primary", key="register_venue", use_container_width=True):
            navigate("add_edit_court", editing_court_id=None)
