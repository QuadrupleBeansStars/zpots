"""Pricing Setup - Base rates and AI dynamic pricing."""
import streamlit as st
from components.css import inject_global_css, inject_owner_sidebar_css
from components.nav import navigate, render_owner_sidebar
from components.cards import kpi_card
from components.charts import pricing_elasticity_chart


def render():
    inject_global_css()
    inject_owner_sidebar_css()
    render_owner_sidebar()

    st.markdown("""
    <h1 style="font-size:2rem; margin-bottom:0;">Pricing Setup</h1>
    <p style="color:#3d4455; font-size:14px;">Precision control for your venue revenue. Leverage our proprietary Kinetic AI to optimize hourly rates based on real-time city demand.</p>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)

    left_col, right_col = st.columns([1.2, 1])

    with left_col:
        st.markdown("""
        <div class="zpots-card">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem;">
                <div>
                    <h3 style="font-size:1.1rem; margin:0;">Base Hourly Rates</h3>
                    <div style="font-family:'Lexend'; font-size:10px; text-transform:uppercase; letter-spacing:0.1em; color:#3d4455;">MANUAL FOUNDATION</div>
                </div>
                <span style="font-size:1.2rem;">💰</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="zpots-card-surface" style="margin-bottom:8px;">
            <div style="font-family:'Inter'; font-weight:600; font-size:14px;">Standard Court</div>
            <div style="font-size:12px; color:#3d4455;">Weekdays 08:00 - 17:00</div>
        </div>
        """, unsafe_allow_html=True)
        st.number_input("Standard (THB)", value=450, step=50, key="standard_price", label_visibility="collapsed")

        st.markdown("""
        <div class="zpots-card-surface" style="margin-bottom:8px; margin-top:8px;">
            <div style="font-family:'Inter'; font-weight:600; font-size:14px;">Prime Time</div>
            <div style="font-size:12px; color:#3d4455;">Daily 17:00 - 23:00</div>
        </div>
        """, unsafe_allow_html=True)
        st.number_input("Prime (THB)", value=650, step=50, key="prime_price", label_visibility="collapsed")

        st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)

        st.markdown("""
        <div class="zpots-card" style="display:flex; justify-content:space-between; align-items:center;">
            <div style="display:flex; align-items:center; gap:8px;">
                <span style="font-size:1.2rem;">🤖</span>
                <div>
                    <div style="font-family:'Inter'; font-weight:600;">AI Dynamic Pricing</div>
                    <div style="font-size:12px; color:#3d4455;">Auto-adjust rates based on booking velocity</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.toggle("Enable", value=True, key="ai_pricing_toggle", label_visibility="collapsed")

        st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)
        comp_col, occ_col = st.columns(2)
        with comp_col:
            kpi_card("COMPETITOR AVERAGE", "510 THB/hr", delta="Your pricing is 12% below market")
        with occ_col:
            kpi_card("OCCUPANCY FORECAST", "92%", delta="HIGH DEMAND EXPECTED")

    with right_col:
        st.markdown("""
        <div class="zpots-card-lime" style="padding:1.5rem;">
            <span class="ai-tag" style="background:rgba(75,94,0,0.15); margin-bottom:8px;">LIVE AI INSIGHT</span>
            <h3 style="font-size:1.3rem; margin-top:8px; color:#1a2600 !important;">Demand Prediction<br>+30% for Friday Evening</h3>
            <p style="font-size:13px; color:#1a2600; margin-top:8px;">Local tournaments and social events in your area are spiking demand for October 27th. Our kinetic model suggests a tactical rate adjustment to maximize yield.</p>
            <hr style="border-color:rgba(75,94,0,0.2);">
            <div style="margin-top:12px;">
                <span style="font-family:'Lexend'; font-size:9px; text-transform:uppercase; letter-spacing:0.1em; color:#1a2600;">SUGGESTED PRICE ADJUSTMENT</span>
                <div style="display:flex; align-items:center; gap:8px; margin-top:4px;">
                    <span style="font-size:12px; color:#1a2600; text-decoration:line-through;">450 THB</span>
                    <span style="font-family:'Space Grotesk'; font-weight:700; font-size:2rem; color:#1a2600;">580 THB</span>
                    <span style="font-size:18px;">⚡</span>
                </div>
                <div style="font-size:12px; color:#1a2600; margin-top:8px;">💰 +2,400 THB projected daily revenue</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Apply Suggested Pricing →", type="primary", key="apply_pricing", width='stretch'):
            st.toast("AI pricing applied!")

        st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)
        st.markdown('<div class="zpots-card"><div style="font-family:\'Lexend\'; font-size:10px; text-transform:uppercase; letter-spacing:0.1em; color:#3d4455;">PRICING ELASTICITY</div></div>', unsafe_allow_html=True)
        st.plotly_chart(pricing_elasticity_chart(), width='stretch', config={"displayModeBar": False})
