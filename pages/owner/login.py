"""Owner Login Screen - Manage Your Arena."""
import streamlit as st
from components.css import inject_global_css, inject_login_css
from components.nav import navigate


def render():
    inject_global_css()
    inject_login_css()
    st.markdown('<style>section[data-testid="stSidebar"]{display:none;}</style>',
                unsafe_allow_html=True)

    st.markdown("<div style='height:2rem;'></div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.3, 1])
    with col2:
        st.markdown("""
        <div style="background:rgba(255,255,255,0.94);backdrop-filter:blur(24px);
                    -webkit-backdrop-filter:blur(24px);border-radius:20px;
                    padding:40px 40px 8px;box-shadow:0 8px 24px rgba(0,0,0,0.3);">
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:14px;">
                <span style="font-family:'Space Grotesk';font-weight:700;font-size:18px;
                             color:#1c2526;letter-spacing:0.05em;">⚡ ZPOTS Admin</span>
            </div>
            <span class="ai-tag">ELITE VENUE PARTNER</span>
            <h1 style="font-family:'Space Grotesk';font-size:2rem;line-height:1.1;
                       margin-top:12px;color:#1c2526 !important;font-weight:700;">
                Venue Control,<br>Supercharged.</h1>
            <p style="color:#3d4455 !important;font-size:14px;margin-top:8px;margin-bottom:0;">
                Sign in to manage your Bangkok sports facilities.</p>
        </div>
        """, unsafe_allow_html=True)

        email    = st.text_input("EMAIL",    placeholder="owner@zpots.ai",        key="owner_email")
        password = st.text_input("PASSWORD", type="password", placeholder="••••••••", key="owner_password")

        if st.button("ENTER CONSOLE →", type="primary", width='stretch', key="owner_login_btn"):
            st.session_state.logged_in = True
            st.session_state.flow = "owner"
            navigate("owner_dashboard")

        st.markdown("""
        <div style="text-align:center;margin-top:1.5rem;margin-bottom:8px;
                    font-size:13px;color:#3d4455;">
            New operator?
            <strong style="color:#1E4A00;cursor:pointer;">Manage your venues</strong>
        </div>
        """, unsafe_allow_html=True)
