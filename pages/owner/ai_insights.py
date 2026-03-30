"""AI Insights - Demand analysis and predictions."""
import streamlit as st
from components.css import inject_global_css, inject_owner_sidebar_css
from components.nav import navigate, render_owner_sidebar
from components.cards import kpi_card
from components.charts import demand_radar_chart, peak_utilization_chart
from data.dummy_data import DISTRICT_DEMAND


def render():
    inject_global_css()
    inject_owner_sidebar_css()
    render_owner_sidebar()

    st.markdown("""
    <div style="display:flex; align-items:center; gap:12px; margin-bottom:0.5rem;">
        <h1 style="font-size:2rem; margin:0;">AI INSIGHTS</h1>
        <span class="status-badge status-active" style="background:rgba(207,252,0,0.3); padding:4px 12px; border-radius:999px; font-size:10px;">ELITE VENUE PARTNER</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)

    heat_col, peak_col = st.columns([1.5, 1])

    with heat_col:
        st.markdown("""
        <div class="zpots-card" style="padding:1.5rem;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem;">
                <div>
                    <h3 style="font-size:1.1rem; margin:0;">Bangkok Demand Heatmap</h3>
                    <div style="font-family:'Lexend'; font-size:10px; text-transform:uppercase; letter-spacing:0.1em; color:#535b71;">LIVE AI PROJECTION • NEXT 24 HOURS</div>
                </div>
                <div style="display:flex; gap:4px;">
                    <span class="status-badge status-cancelled" style="background:rgba(176,37,0,0.1); color:#b02500; padding:4px 8px; border-radius:999px; font-size:9px;">CRITICAL</span>
                    <span class="status-badge status-active" style="background:rgba(207,252,0,0.3); padding:4px 8px; border-radius:999px; font-size:9px;">OPTIMAL</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.plotly_chart(demand_radar_chart(DISTRICT_DEMAND), use_container_width=True, config={"displayModeBar": False})

        dist_cols = st.columns(3)
        for i, district in enumerate(DISTRICT_DEMAND):
            with dist_cols[i]:
                level_color = "#cffc00" if district["level"] == "Peak" else "#e2e7ff" if district["level"] == "Moderate" else "#ffddcc"
                st.markdown(f"""
                <div class="zpots-card-surface" style="text-align:center; padding:1rem;">
                    <div style="font-family:'Lexend'; font-size:9px; text-transform:uppercase; letter-spacing:0.1em; color:#535b71;">{district['name']}</div>
                    <div style="font-family:'Space Grotesk'; font-weight:700; font-size:1.5rem; margin:4px 0;">{district['demand']}%</div>
                    <span class="status-badge" style="background:{level_color}; padding:4px 10px; border-radius:999px; font-size:9px;">{district['level']}</span>
                </div>
                """, unsafe_allow_html=True)

    with peak_col:
        st.markdown("""
        <div class="zpots-card">
            <h3 style="font-size:1rem; margin-bottom:4px;">Peak Utilization</h3>
            <div style="font-family:'Lexend'; font-size:10px; text-transform:uppercase; letter-spacing:0.1em; color:#535b71;">HOURLY DISTRIBUTION (MON-SUN)</div>
        </div>
        """, unsafe_allow_html=True)
        st.plotly_chart(peak_utilization_chart(), use_container_width=True, config={"displayModeBar": False})

        st.markdown("""
        <div class="zpots-card" style="margin-top:0.5rem;">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:4px;">
                <span style="color:#cffc00; font-size:14px;">⚡</span>
                <span style="font-family:'Inter'; font-weight:600;">Golden Slot</span>
                <span style="font-family:'Inter'; font-weight:700; color:#506300;">฿2,400/hr</span>
            </div>
            <div style="font-size:12px; color:#535b71;">(19:00)</div>
            <hr>
            <div style="display:flex; align-items:center; gap:8px;">
                <span style="color:#535b71; font-size:12px;">⏳</span>
                <span style="font-size:12px; color:#535b71;">Off-Peak (14:00)</span>
                <span style="font-family:'Inter'; font-weight:600;">฿1,200/hr</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:1.5rem;'></div>", unsafe_allow_html=True)

    noshow_col, mitigation_col = st.columns(2)

    with noshow_col:
        st.markdown("""
        <div class="zpots-card">
            <h3 style="font-size:1.1rem; margin-bottom:4px;">No-Show Risk Analysis ⚠️</h3>
            <div style="font-family:'Lexend'; font-size:10px; text-transform:uppercase; letter-spacing:0.1em; color:#b02500; margin-bottom:12px;">PRIORITY: HIGH INTERVENTION</div>
            <div class="zpots-card-surface" style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                <span style="font-size:13px;">Probable No-Shows</span>
                <span style="font-family:'Space Grotesk'; font-weight:700; font-size:16px;">12% <span style="font-size:12px; color:#b02500;">(+4% WoW)</span></span>
            </div>
            <div class="zpots-card-surface" style="padding:1rem;">
                <div style="font-family:'Lexend'; font-size:10px; text-transform:uppercase; letter-spacing:0.1em; color:#535b71;">PRIMARY ROOT CAUSE</div>
                <div style="font-size:13px; color:#272e42; margin-top:4px;">Traffic delays on Rama IV during rain predicted (70% probability).</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with mitigation_col:
        st.markdown("""
        <div class="zpots-card-surface" style="padding:1.5rem;">
            <h3 style="font-size:1.1rem; margin-bottom:1rem;">AI Mitigation Strategies</h3>
            <div style="display:flex; gap:1rem;">
                <div class="zpots-card" style="flex:1;">
                    <h4 style="font-size:14px; margin-bottom:4px;">Smart Reschedule</h4>
                    <p style="font-size:12px; color:#535b71;">Auto-offer 15-min delay window to users in high-traffic zones to prevent abandonment.</p>
                    <span style="font-family:'Lexend'; font-size:9px; color:#506300;">ESTIMATED IMPACT: +23% Retention</span>
                </div>
                <div class="zpots-card" style="flex:1;">
                    <h4 style="font-size:14px; margin-bottom:4px;">Pre-Check Deposit</h4>
                    <p style="font-size:12px; color:#535b71;">Implement 20% commitment fee for high-demand Saturday slots for users with > 80% reliability.</p>
                    <span style="font-family:'Lexend'; font-size:9px; color:#506300;">ESTIMATED IMPACT: -60% No-Shows</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Execute All", type="primary", key="execute_all"):
            st.toast("AI strategies deployed!")

    st.markdown("<div style='height:1.5rem;'></div>", unsafe_allow_html=True)

    bottom_cols = st.columns(4)
    with bottom_cols[0]:
        kpi_card("TOTAL MONTHLY REVENUE", "฿482k", delta="↗ +12.4% vs Last Month", icon="💰")
    with bottom_cols[1]:
        kpi_card("AVG. SLOT OCCUPANCY", "78%", delta="⊡ Stable (+0.2%)", icon="📊")
    with bottom_cols[2]:
        kpi_card("CUSTOMER RATING", "4.9 ⭐⭐⭐⭐⭐", delta="Top 1% of Venue Partners", icon="⭐")
    with bottom_cols[3]:
        kpi_card("AI EFFICIENCY SCORE", "92/100", delta="Optimal Pricing Achieved", icon="🤖")
