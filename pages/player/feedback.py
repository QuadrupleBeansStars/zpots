"""Leave Feedback Screen."""
import streamlit as st
from components.css import inject_global_css
from components.nav import navigate, render_player_topbar
from data.dummy_data import FEEDBACK_TAGS


def render():
    inject_global_css()
    render_player_topbar()

    st.markdown("# Rate your Session")

    st.markdown('<div style="font-family:\'Lexend\'; font-size:10px; text-transform:uppercase; letter-spacing:0.1em; color:#3d4455; margin-bottom:8px;">OVERALL RATING</div>', unsafe_allow_html=True)

    if "feedback_stars" not in st.session_state:
        st.session_state.feedback_stars = 4

    star_cols = st.columns(5)
    for i in range(5):
        with star_cols[i]:
            filled = i < st.session_state.feedback_stars
            star = "⭐" if filled else "☆"
            if st.button(star, key=f"star_{i}", width='stretch'):
                st.session_state.feedback_stars = i + 1
                st.rerun()

    st.markdown("<div style='height:1.5rem;'></div>", unsafe_allow_html=True)

    st.markdown('<div style="font-family:\'Lexend\'; font-size:10px; text-transform:uppercase; letter-spacing:0.1em; color:#3d4455; margin-bottom:8px;">WHAT WENT WELL?</div>', unsafe_allow_html=True)

    if "feedback_selected_tags" not in st.session_state:
        st.session_state.feedback_selected_tags = ["Clean Courts", "Good Lighting"]

    tag_cols = st.columns(len(FEEDBACK_TAGS))
    for i, tag in enumerate(FEEDBACK_TAGS):
        with tag_cols[i]:
            is_selected = tag in st.session_state.feedback_selected_tags
            btn_type = "primary" if is_selected else "secondary"
            if st.button(tag, key=f"tag_{i}", type=btn_type, width='stretch'):
                if is_selected:
                    st.session_state.feedback_selected_tags.remove(tag)
                else:
                    st.session_state.feedback_selected_tags.append(tag)
                st.rerun()

    st.markdown("<div style='height:1.5rem;'></div>", unsafe_allow_html=True)
    st.markdown('<div style="font-family:\'Lexend\'; font-size:10px; text-transform:uppercase; letter-spacing:0.1em; color:#3d4455; margin-bottom:8px;">LEAVE A REVIEW (OPTIONAL)</div>', unsafe_allow_html=True)

    review = st.text_area(
        "Review",
        placeholder="Tell us about the court surface, ventilation, or atmosphere...",
        height=150,
        key="feedback_review",
        label_visibility="collapsed",
    )

    st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)

    if st.button("Submit Feedback →", type="primary", key="submit_feedback", width='stretch'):
        st.toast("Thank you for your feedback!")
        st.balloons()
        navigate("my_bookings")

    st.markdown('<div style="text-align:center; font-size:12px; color:#3d4455; margin-top:8px;">Earn 50 ZPOTS Kinetic Points for this review.</div>', unsafe_allow_html=True)
