"""Manage Slots - Weekly calendar view."""
import streamlit as st
from components.css import inject_global_css, inject_owner_sidebar_css
from components.nav import navigate, render_owner_sidebar
from components.cards import kpi_card
from data.dummy_data import SLOT_CALENDAR


def render():
    inject_global_css()
    inject_owner_sidebar_css()
    render_owner_sidebar()

    hcol1, hcol2, hcol3 = st.columns([2, 1, 1])
    with hcol1:
        st.markdown('<h1 style="font-size:2rem; margin-bottom:0;">Slot Control</h1>', unsafe_allow_html=True)
        st.markdown('<span class="ai-tag">LIVE AI OPTIMIZATION ON</span>', unsafe_allow_html=True)
    with hcol2:
        st.markdown('<div style="text-align:right; font-family:\'Space Grotesk\'; font-size:1.2rem; font-weight:600;">May 12–18</div>', unsafe_allow_html=True)
    with hcol3:
        if st.button("Add New Slot", type="primary", key="add_slot"):
            st.toast("Slot creation form opened!")

    st.markdown('<p style="color:#3d4455; font-size:14px;">Precision management of court inventory. AI is currently forecasting 97% occupancy for weekend prime slots.</p>', unsafe_allow_html=True)

    days = ["MON<br>12", "TUE<br>13", "WED<br>14", "THU<br>15", "FRI<br>16", "SAT<br>17", "SUN<br>18"]
    day_cols = st.columns(7)

    for i, day in enumerate(days):
        with day_cols[i]:
            is_active = i == 2
            bg = "#cffc00" if is_active else "#eef0ff"
            text_color = "#1a2600" if is_active else "#3d4455"
            st.markdown(f'<div style="text-align:center; font-family:\'Lexend\'; font-size:10px; text-transform:uppercase; letter-spacing:0.08em; color:{text_color}; padding:8px 0; background:{bg}; border-radius:8px; margin-bottom:8px;">{day}</div>', unsafe_allow_html=True)

            slots = SLOT_CALENDAR.get(i, [])
            if slots:
                for slot in slots:
                    st.markdown(f"""
                    <div style="background:{slot['color']}; border-radius:8px; padding:8px; margin-bottom:6px; font-size:11px;">
                        <div style="font-weight:600; color:#272e42;">{slot['label']}</div>
                        <div style="color:#3d4455; font-size:10px;">{slot['time']}</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown('<div style="background:#f6f6ff; border-radius:8px; padding:16px; text-align:center; color:#a5adc6; font-size:20px; cursor:pointer;">+</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:1.5rem;'></div>", unsafe_allow_html=True)
    st.markdown('<h3 style="font-size:1rem;">🤖 AI Performance Prediction</h3>', unsafe_allow_html=True)

    pred_cols = st.columns(4)
    with pred_cols[0]:
        kpi_card("PREDICTED REVENUE", "$4,280.00", delta="↗ +10% vs LW", icon="💰")
    with pred_cols[1]:
        kpi_card("PEAK HOURS", "18:00–20:00", delta="Fri, Sat, Sun", icon="🕐")
    with pred_cols[2]:
        kpi_card("OCCUPANCY", "88.4%", icon="📊")
    with pred_cols[3]:
        kpi_card("ACTIVE SLOTS", "24 Active", delta="View Rewards", icon="📅")

    st.markdown("<div style='height:1.5rem;'></div>", unsafe_allow_html=True)
    st.markdown('<div class="zpots-card"><h3 style="font-size:1rem; margin-bottom:1rem;">Quick Controls</h3></div>', unsafe_allow_html=True)

    ctrl_cols = st.columns(3)
    with ctrl_cols[0]:
        st.toggle("Auto-Fill Waitlist", value=True, key="auto_fill")
    with ctrl_cols[1]:
        st.toggle("Dynamic Pricing", value=True, key="dynamic_pricing_toggle")
    with ctrl_cols[2]:
        st.toggle("Public Visibility", value=True, key="public_visibility")
