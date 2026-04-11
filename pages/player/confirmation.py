"""Booking Confirmation Screen."""
import streamlit as st
from components.css import inject_global_css
from components.nav import navigate, render_player_topbar
from data.dummy_data import COURTS, PLAYER_BOOKINGS
from utils.gemini import chat_with_court_assistant


def render():
    inject_global_css()
    render_player_topbar()

    booking = PLAYER_BOOKINGS[0]
    court = next((c for c in COURTS if c["id"] == booking["court_id"]), COURTS[0])

    left_col, right_col = st.columns([1, 1])

    with left_col:
        st.markdown(f"""
        <div style="margin-top:2rem;">
            <div style="width:48px; height:48px; border-radius:50%; background:#cffc00; display:flex; align-items:center; justify-content:center; font-size:24px; margin-bottom:1rem;">✓</div>
            <h1 style="font-size:3rem; line-height:1.05; margin-bottom:0.5rem;">Booking<br><span style="color:#506300;">Confirmed!</span></h1>
            <p style="font-size:15px; color:#3d4455; margin-bottom:2rem;">You're all set for <strong>{court['name']}</strong>. Your court is waiting.</p>
        </div>
        """, unsafe_allow_html=True)

        bcol1, bcol2 = st.columns(2)
        with bcol1:
            if st.button("View My Bookings", type="primary", key="view_bookings"):
                navigate("my_bookings")
        with bcol2:
            if st.button("📅 Add to Calendar", key="add_calendar"):
                st.toast("Added to calendar!")

        st.markdown("<div style='height:2rem;'></div>", unsafe_allow_html=True)

        st.markdown("""
        <h3 style="font-size:1rem;">Invite your team</h3>
        <p style="font-size:13px; color:#3d4455;">Share the booking details and get ready for the match.</p>
        """, unsafe_allow_html=True)

        icols = st.columns(4)
        with icols[0]:
            st.button("📤 Share", key="share_btn")
        with icols[1]:
            st.button("📋 Copy", key="copy_btn")
        with icols[2]:
            st.button("📧 Email", key="email_btn")

    with right_col:
        st.markdown(f"""
        <div class="zpots-card" style="margin-bottom:1rem;">
            <div style="font-family:'Lexend'; font-size:10px; text-transform:uppercase; letter-spacing:0.1em; color:#3d4455;">TRANSACTION ID</div>
            <div style="font-family:'Space Grotesk'; font-weight:700; font-size:1.5rem; color:#272e42;">#{booking['id']}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="zpots-card" style="padding:0; overflow:hidden;">
            <div class="court-image" style="background:linear-gradient(135deg, {court['color']}, {court['color']}cc); height:140px; position:relative;">
                <span class="ai-tag" style="position:absolute; bottom:12px; left:12px;">AI VERIFIED SLOT</span>
                <div style="position:absolute; bottom:12px; right:12px; color:white; font-family:'Inter'; font-weight:600; font-size:14px;">{court['name']}</div>
            </div>
            <div style="padding:1rem;">
                <div style="display:flex; gap:2rem;">
                    <div>
                        <div style="font-family:'Lexend'; font-size:9px; text-transform:uppercase; letter-spacing:0.1em; color:#3d4455;">TIME SLOT</div>
                        <div style="font-family:'Space Grotesk'; font-weight:700; font-size:16px;">{booking['time_start']} – {booking['time_end']}</div>
                        <div style="font-size:12px; color:#3d4455;">Tomorrow, Oct 24</div>
                    </div>
                    <div>
                        <div style="font-family:'Lexend'; font-size:9px; text-transform:uppercase; letter-spacing:0.1em; color:#3d4455;">COURT DETAILS</div>
                        <div style="font-family:'Space Grotesk'; font-weight:700; font-size:16px;">Court {booking['court_number']}</div>
                        <div style="font-size:12px; color:#3d4455;">{booking['surface']}</div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="zpots-card" style="display:flex; align-items:center; justify-content:space-between;">
            <div style="display:flex; align-items:center; gap:12px;">
                <span style="font-size:1.5rem;">📍</span>
                <div>
                    <div style="font-family:'Inter'; font-weight:600; font-size:14px;">{booking['address']}</div>
                    <div style="font-size:12px; color:#3d4455;">{booking['address_note']}</div>
                </div>
            </div>
            <span style="color:#506300; font-size:18px;">◆</span>
        </div>
        """, unsafe_allow_html=True)

    # --- Post-Booking Chat Assistant (compact widget) ---
    st.space("medium")

    if "booking_chat" not in st.session_state:
        st.session_state.booking_chat = []

    _, chat_col, _ = st.columns([1, 2, 1])
    with chat_col:
        with st.container(border=True):
            st.markdown(":material/chat: **Have questions about your booking?**")
            st.caption("Ask about directions, parking, what to bring, BTS access, and more.")

            if st.session_state.booking_chat:
                for msg in st.session_state.booking_chat:
                    with st.chat_message(msg["role"]):
                        st.markdown(msg["content"])

            q_col, btn_col = st.columns([5, 1])
            with q_col:
                user_input = st.text_input(
                    "chat",
                    placeholder="Ask about directions, parking...",
                    label_visibility="collapsed",
                    key="booking_chat_input",
                )
            with btn_col:
                send = st.button("Send", type="primary", use_container_width=True, key="chat_send")

            if send and user_input.strip():
                msg = user_input.strip()
                st.session_state.booking_chat.append({"role": "user", "content": msg})
                with st.spinner(""):
                    reply = chat_with_court_assistant(st.session_state.booking_chat, court, booking)
                st.session_state.booking_chat.append({"role": "assistant", "content": reply})
                st.rerun()
