"""Player Login Screen - Welcome Back, Athlete."""
import streamlit as st
from components.css import inject_global_css, inject_login_css
from components.nav import navigate


def render():
    inject_global_css()
    inject_login_css()
    st.markdown('<style>section[data-testid="stSidebar"]{display:none;}</style>',
                unsafe_allow_html=True)

    # Logo
    st.markdown("""
    <div style="display:flex; align-items:center; gap:10px; justify-content:center;
                padding-top:2.5rem; padding-bottom:0.5rem;">
        <span style="font-family:'Space Grotesk';font-weight:700;font-size:1.4rem;
                     color:white;letter-spacing:0.06em;">⚡ ZPOTS</span>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.3, 1])
    with col2:
        # Glass card header (rendered as HTML; inputs below use Streamlit widgets)
        st.markdown("""
        <div style="background:rgba(255,255,255,0.94);backdrop-filter:blur(24px);
                    -webkit-backdrop-filter:blur(24px);border-radius:20px;
                    padding:40px 40px 8px;box-shadow:0 8px 24px rgba(0,0,0,0.25);">
            <h1 style="font-family:'Space Grotesk';font-size:2.1rem;line-height:1.1;
                       color:#1c2526 !important;font-weight:700;margin:0;">
                Welcome Back,<br>Athlete</h1>
            <p style="color:#3d4455 !important;font-size:14px;margin-top:8px;margin-bottom:0;">
                Log in to book your next game.</p>
        </div>
        """, unsafe_allow_html=True)

        email    = st.text_input("EMAIL",    placeholder="athlete@zpots.ai",   key="player_email")
        password = st.text_input("PASSWORD", type="password", placeholder="••••••••", key="player_password")

        if st.button("LOG IN", type="primary", width='stretch', key="player_login_btn"):
            st.session_state.logged_in = True
            st.session_state.flow = "player"
            navigate("player_home")

        st.markdown("""
        <div style="text-align:center;color:#3d4455;font-size:13px;margin:18px 0 12px;">
            or continue with</div>
        """, unsafe_allow_html=True)

        gcol1, gcol2 = st.columns(2)
        with gcol1:
            if st.button("Google", width='stretch', key="google_login"):
                st.session_state.logged_in = True
                st.session_state.flow = "player"
                navigate("player_home")
        with gcol2:
            if st.button("Facebook", width='stretch', key="fb_login"):
                st.session_state.logged_in = True
                st.session_state.flow = "player"
                navigate("player_home")

        st.markdown("""
        <div style="text-align:center;margin-top:18px;margin-bottom:8px;
                    font-size:13px;color:#3d4455;">
            Don't have an account?
            <b style="color:#1E4A00;cursor:pointer;">Sign Up</b>
        </div>
        """, unsafe_allow_html=True)

    # Fixed live status badge
    st.markdown("""
    <div style="position:fixed;bottom:20px;right:20px;z-index:999;
                background:#fff;padding:8px 16px;border-radius:999px;
                display:inline-flex;align-items:center;gap:8px;
                box-shadow:0 4px 16px rgba(0,0,0,0.2);">
        <span class="ai-tag" style="font-size:9px;">LIVE STATUS</span>
        <span style="font-family:'Space Grotesk';font-weight:700;font-size:13px;
                     color:#1c2526;">412 Courts Available</span>
    </div>
    """, unsafe_allow_html=True)
