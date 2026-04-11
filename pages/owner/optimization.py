"""Optimization Engine - Live opportunities and recommendations."""
import streamlit as st
from components.css import inject_global_css, inject_owner_sidebar_css
from components.nav import navigate, render_owner_sidebar


def render():
    inject_global_css()
    inject_owner_sidebar_css()
    render_owner_sidebar()

    st.markdown("""
    <h1 style="font-size:2rem; margin-bottom:0;">Optimization Engine</h1>
    <div style="font-family:'Lexend'; font-size:10px; text-transform:uppercase; letter-spacing:0.1em; color:#3d4455; margin-top:4px;">AI OPS › PRIORITY INSIGHT</div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)

    rec_col, outcome_col = st.columns([1.5, 1])

    with rec_col:
        st.markdown("""
        <div class="zpots-card" style="padding:2rem;">
            <span class="ai-tag" style="margin-bottom:12px;">LIVE OPPORTUNITY</span>
            <h2 style="font-size:1.8rem; line-height:1.15; margin-top:12px;">Adjust availability for<br><span style="color:#506300; font-style:italic;">Sunday Morning</span> to capture<br><span style="color:#506300;">+20%</span> demand.</h2>
            <div style="margin-top:1rem; font-size:20px; color:#506300; font-family:'Space Grotesk'; font-weight:700;">+20%<br><span style="font-size:12px; font-weight:400; color:#3d4455;">REVENUE LIFT</span></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)

        st.markdown("""
        <div class="zpots-card-surface" style="padding:1.2rem;">
            <p style="font-size:14px; color:#3d4455;">Data from the last 4 weeks shows a consistent search spike for Sunday 8:00 AM – 11:00 AM. Currently, your slots are locked for club training.</p>
            <div style="display:flex; align-items:center; gap:8px; margin-top:12px;">
                <span style="color:#506300; font-size:14px;">✓</span>
                <span style="font-size:13px; color:#272e42;">Releasing 3 courts will likely fill within 12 hours.</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)

        bcol1, bcol2 = st.columns(2)
        with bcol1:
            if st.button("Adjust Slots Now ⚡", type="primary", key="adjust_slots", width='stretch'):
                st.toast("Slots adjusted! 3 courts released for Sunday morning.")
                navigate("manage_slots")
        with bcol2:
            if st.button("Dismiss Insight", key="dismiss"):
                st.toast("Insight dismissed.")

    with outcome_col:
        st.markdown("""
        <div class="zpots-card-lime" style="padding:1.5rem;">
            <div style="font-family:'Lexend'; font-size:10px; text-transform:uppercase; letter-spacing:0.1em; color:#1a2600; margin-bottom:12px;">PREDICTED OUTCOMES</div>
            <div style="margin-bottom:16px;">
                <div style="font-family:'Lexend'; font-size:9px; text-transform:uppercase; letter-spacing:0.1em; color:#1a2600;">WEEKLY EARNINGS</div>
                <div style="display:flex; align-items:baseline; gap:8px;">
                    <span style="font-family:'Space Grotesk'; font-weight:700; font-size:2rem; color:#1a2600;">$1,420</span>
                    <span style="font-size:12px; color:#506300;">+$204</span>
                </div>
            </div>
            <div>
                <div style="font-family:'Lexend'; font-size:9px; text-transform:uppercase; letter-spacing:0.1em; color:#1a2600;">OCCUPANCY RATE</div>
                <div style="display:flex; align-items:baseline; gap:8px;">
                    <span style="font-family:'Space Grotesk'; font-weight:700; font-size:2rem; color:#1a2600;">92%</span>
                    <span style="font-size:12px; color:#506300;">↑ 8%</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)

        st.markdown("""
        <div class="court-image" style="background:linear-gradient(135deg, #2a2a2a, #3a3a3a); height:150px;">
            <span style="font-size:2rem;">🏟</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div style="font-size:11px; color:#3d4455; margin-top:8px; font-style:italic;">AI confidence score <strong>94%</strong> based on 1.2k local user search signals.</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:2rem;'></div>", unsafe_allow_html=True)

    bottom_cols = st.columns(3)
    with bottom_cols[0]:
        st.markdown("""
        <div class="zpots-card">
            <span style="font-size:1.2rem;">📊</span>
            <div style="font-family:'Lexend'; font-size:9px; text-transform:uppercase; letter-spacing:0.1em; color:#3d4455; margin-top:8px;">MARKET BENCHMARK</div>
            <p style="font-size:13px; color:#3d4455; margin-top:8px;">Similar venues in your area are pricing Sunday mornings at <strong>$45/hr</strong>.</p>
            <div style="font-family:'Inter'; font-size:13px; margin-top:4px;">Your: <strong>$38/hr</strong></div>
        </div>
        """, unsafe_allow_html=True)
    with bottom_cols[1]:
        st.markdown("""
        <div class="zpots-card">
            <span style="font-size:1.2rem;">👥</span>
            <div style="font-family:'Lexend'; font-size:9px; text-transform:uppercase; letter-spacing:0.1em; color:#3d4455; margin-top:8px;">USER LOYALTY</div>
            <p style="font-size:13px; color:#3d4455; margin-top:8px;">Weekend users are <strong>3.5x</strong> more likely to book a recurring monthly slot.</p>
            <div style="font-size:12px; color:#506300; margin-top:4px;">High LTV potential</div>
        </div>
        """, unsafe_allow_html=True)
    with bottom_cols[2]:
        st.markdown("""
        <div class="zpots-card">
            <span style="font-size:1.2rem;">⏰</span>
            <div style="font-family:'Lexend'; font-size:9px; text-transform:uppercase; letter-spacing:0.1em; color:#3d4455; margin-top:8px;">LEAD TIME</div>
            <p style="font-size:13px; color:#3d4455; margin-top:8px;">Users are searching for Sunday slots as early as <strong>Wednesday evening</strong>.</p>
            <div style="font-size:12px; color:#506300; margin-top:4px;">Optimize now</div>
        </div>
        """, unsafe_allow_html=True)
