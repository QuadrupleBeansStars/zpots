"""Player Login Screen - Welcome Back, Athlete."""
import streamlit as st
from components.css import inject_global_css, inject_login_css
from components.nav import navigate


def render():
    inject_global_css()
    inject_login_css()

    st.markdown("""
    <div style="text-align:center; padding-top:2rem;">
        <span style="font-family:'Space Grotesk', sans-serif; font-weight:700; font-size:1.5rem; color:white; letter-spacing:0.05em;">ZPOTS</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:2rem;'></div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("""
        <div class="glass-card" style="background:rgba(255,255,255,0.92); padding:2.5rem;">
            <h1 style="font-size:2.2rem; margin-bottom:0.2rem; color:#272e42 !important;">Welcome Back,<br>Athlete</h1>
            <p style="color:#535b71 !important; font-size:14px; margin-bottom:1.5rem;">Log in to book your next game.</p>
        </div>
        """, unsafe_allow_html=True)

        email = st.text_input("EMAIL", placeholder="athlete@zpots.ai", key="player_email")
        password = st.text_input("PASSWORD", type="password", placeholder="••••••••", key="player_password")

        st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)

        if st.button("LOG IN", type="primary", use_container_width=True, key="player_login_btn"):
            st.session_state.logged_in = True
            st.session_state.flow = "player"
            navigate("player_home")

        st.markdown("""
        <div style="text-align:center; margin:1rem 0; color:rgba(255,255,255,0.5); font-size:13px;">or continue with</div>
        """, unsafe_allow_html=True)

        gcol1, gcol2 = st.columns(2)
        with gcol1:
            if st.button("Google", use_container_width=True, key="google_login"):
                st.session_state.logged_in = True
                st.session_state.flow = "player"
                navigate("player_home")
        with gcol2:
            if st.button("Facebook", use_container_width=True, key="fb_login"):
                st.session_state.logged_in = True
                st.session_state.flow = "player"
                navigate("player_home")

        st.markdown("""
        <div style="text-align:center; margin-top:1.5rem; font-size:13px; color:rgba(255,255,255,0.7);">
            Don't have an account? <strong style="color:white; cursor:pointer;">Sign Up</strong>
        </div>
        """, unsafe_allow_html=True)

    # Live status badge
    st.markdown("""
    <div style="position:fixed; bottom:2rem; right:2rem;">
        <div class="zpots-card" style="padding:8px 16px; display:inline-flex; align-items:center; gap:8px;">
            <span class="ai-tag" style="font-size:9px;">LIVE STATUS</span>
            <span style="font-family:'Space Grotesk'; font-weight:700; font-size:14px; color:#272e42;">412 Courts Available</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
