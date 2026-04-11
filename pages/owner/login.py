"""Owner Login Screen - Manage Your Arena."""
import streamlit as st
from components.css import inject_global_css, inject_login_css
from components.nav import navigate


def render():
    inject_global_css()
    inject_login_css()

    left_col, right_col = st.columns([1.2, 1])

    with left_col:
        st.markdown("""
        <div style="padding-top:2rem;">
            <span style="font-family:'Space Grotesk'; font-weight:700; font-size:1.3rem; color:white; letter-spacing:0.05em;">ZPOTS.BUSINESS</span>
        </div>
        <div style="margin-top:2rem;">
            <span class="ai-tag" style="background:rgba(207,252,0,0.1);">LIVE AI INSIGHTS ACTIVE</span>
        </div>
        <h1 style="font-size:3rem; line-height:1.05; margin-top:1rem; color:white !important;">Manage Your<br><span style="color:#cffc00;">Arena</span></h1>
        <p style="color:rgba(255,255,255,0.9) !important; font-size:15px; max-width:400px;">Access your owner dashboard and AI insights. Monitor occupancy, revenue, and court health in real-time.</p>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="display:flex; gap:1rem; margin-top:2rem;">
            <div style="padding:12px 16px; background:rgba(255,255,255,0.1); backdrop-filter:blur(12px); border-radius:16px;">
                <span style="font-family:'Lexend'; font-size:9px; text-transform:uppercase; letter-spacing:0.1em; color:rgba(255,255,255,0.9);">LIVE TRAFFIC</span><br>
                <span style="font-family:'Space Grotesk'; font-weight:700; font-size:1.5rem; color:white;">84%</span>
            </div>
            <div style="padding:12px 16px; background:rgba(255,255,255,0.1); backdrop-filter:blur(12px); border-radius:16px;">
                <span style="font-family:'Lexend'; font-size:9px; text-transform:uppercase; letter-spacing:0.1em; color:rgba(255,255,255,0.9);">REV</span><br>
                <span style="font-family:'Space Grotesk'; font-weight:700; font-size:1.5rem; color:#cffc00;">+$420</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with right_col:
        st.markdown("""
        <div class="glass-card" style="margin-top:3rem;">
            <h3 style="font-size:1.3rem; color:#272e42 !important; margin-bottom:4px;">Partner Login</h3>
            <p style="color:#3d4455 !important; font-size:13px; margin-bottom:1.5rem;">Enter your credentials to manage your venue ecosystem.</p>
        </div>
        """, unsafe_allow_html=True)

        email = st.text_input("BUSINESS EMAIL", placeholder="director@arena-complex.com", key="owner_email")
        password = st.text_input("PASSWORD", type="password", placeholder="••••••••••••••", key="owner_password")

        if st.button("Log In to Dashboard →", type="primary", width='stretch', key="owner_login_btn"):
            st.session_state.logged_in = True
            st.session_state.flow = "owner"
            navigate("owner_dashboard")

        st.markdown('<div style="text-align:center; margin:1rem 0; font-size:12px; color:#3d4455;">OR AUTHENTICATE WITH</div>', unsafe_allow_html=True)

        if st.button("🏢 Corporate ID", width='stretch', key="corp_id_login"):
            st.session_state.logged_in = True
            st.session_state.flow = "owner"
            navigate("owner_dashboard")

        st.markdown('<div style="text-align:center; margin-top:1.5rem; font-size:13px; color:#3d4455;">New operator? <strong style="color:#506300; cursor:pointer;">Manage your venues</strong></div>', unsafe_allow_html=True)
