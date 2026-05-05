"""Player Login Screen - Welcome Back, Athlete."""
import streamlit as st
from components.css import inject_global_css, inject_login_css
from components.nav import navigate
from data.database import create_user, get_user_by_email, verify_password


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
        st.markdown("""
        <div style="background:rgba(255,255,255,0.94);backdrop-filter:blur(24px);
                    -webkit-backdrop-filter:blur(24px);border-radius:20px;
                    padding:40px 40px 8px;box-shadow:0 8px 24px rgba(0,0,0,0.25);">
            <h1 style="font-family:'Space Grotesk';font-size:2.1rem;line-height:1.1;
                       color:#1c2526 !important;font-weight:700;margin:0;">
                Welcome Back,<br>Athlete</h1>
            <p style="color:#3d4455 !important;font-size:14px;margin-top:8px;margin-bottom:0;">
                Log in or create an account to book your next game.</p>
        </div>
        """, unsafe_allow_html=True)

        login_tab, register_tab = st.tabs(["Login", "Register"])

        with login_tab:
            email    = st.text_input("EMAIL",    placeholder="athlete@zpots.ai",   key="player_email")
            password = st.text_input("PASSWORD", type="password", placeholder="••••••••", key="player_password")

            if st.button("LOG IN", type="primary", width='stretch', key="player_login_btn"):
                user = get_user_by_email(email.strip().lower()) if email.strip() else None
                if user is None or not verify_password(user, password):
                    st.error("Invalid email or password.")
                elif user["role"] != "player":
                    st.error("This account is registered as an owner. Use Owner login.")
                else:
                    st.session_state.logged_in  = True
                    st.session_state.user_id    = user["id"]
                    st.session_state.user_name  = user["name"]
                    st.session_state.user_email = user["email"]
                    st.session_state.flow = "player"
                    navigate("player_home")

            st.markdown("""
            <div style="text-align:center;color:#3d4455;font-size:13px;margin:18px 0 12px;">
                or continue with</div>
            """, unsafe_allow_html=True)

            gcol1, gcol2 = st.columns(2)
            with gcol1:
                if st.button("Google", width='stretch', key="google_login"):
                    st.toast("OAuth not yet supported — use email/password.", icon="ℹ️")
            with gcol2:
                if st.button("Facebook", width='stretch', key="fb_login"):
                    st.toast("OAuth not yet supported — use email/password.", icon="ℹ️")

            st.markdown("""
            <div style="text-align:center;margin-top:18px;margin-bottom:8px;
                        font-size:13px;color:#3d4455;">
                Demo: <b>player@zpots.ai</b> / <b>demo123</b>
            </div>
            """, unsafe_allow_html=True)

        with register_tab:
            reg_name  = st.text_input("YOUR NAME",        placeholder="Somchai Jaidee",   key="reg_name")
            reg_email = st.text_input("EMAIL",            placeholder="you@example.com",  key="reg_email")
            reg_pass  = st.text_input("PASSWORD",         type="password", placeholder="Min 6 characters", key="reg_pass")
            reg_pass2 = st.text_input("CONFIRM PASSWORD", type="password", placeholder="••••••••",          key="reg_pass2")

            if st.button("CREATE ACCOUNT", type="primary", width='stretch', key="register_btn"):
                name  = reg_name.strip()
                email = reg_email.strip().lower()
                pw    = reg_pass
                pw2   = reg_pass2

                if not all([name, email, pw, pw2]):
                    st.error("All fields are required.")
                elif len(pw) < 6:
                    st.error("Password must be at least 6 characters.")
                elif pw != pw2:
                    st.error("Passwords do not match.")
                elif get_user_by_email(email) is not None:
                    st.error("An account with this email already exists.")
                else:
                    user = create_user(email, name, pw, role="player")
                    st.session_state.logged_in  = True
                    st.session_state.user_id    = user["id"]
                    st.session_state.user_name  = user["name"]
                    st.session_state.user_email = user["email"]
                    st.session_state.flow = "player"
                    navigate("player_home")

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
