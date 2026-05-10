"""Floating player chat widget. Mount once from app.py for player sessions."""
import streamlit as st
from streamlit_float import float_init, float_css_helper

from agents.player.agent import run_turn
from data import database as db


def render_player_chat() -> None:
    user = st.session_state.get("user")
    if not user or user.get("role") != "player":
        return

    float_init()

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
        st.session_state.pending_draft = None
        st.session_state.chat_open = False

    # Floating launcher button
    btn_css = float_css_helper(width="56px", right="20px", bottom="20px", transition=0)
    with st.container():
        if st.button("💬", key="zpots_chat_toggle", help="Chat with ZPOTS assistant"):
            st.session_state.chat_open = not st.session_state.chat_open
    st.markdown(f'<style>{btn_css}</style>', unsafe_allow_html=True)

    if not st.session_state.chat_open:
        return

    # Floating panel
    panel_css = float_css_helper(
        width="360px", height="520px", right="20px", bottom="90px",
        background="white", border="1px solid #ddd", border_radius="12px",
        padding="12px", shadow=12, transition=0,
    )
    panel = st.container()
    with panel:
        st.markdown("**ZPOTS Assistant**")
        for m in st.session_state.chat_history:
            if isinstance(m["content"], str):
                with st.chat_message(m["role"]):
                    st.write(m["content"])

        draft = st.session_state.pending_draft
        if draft:
            _render_draft_confirm(draft, user)

        prompt = st.chat_input("Ask anything…", key="zpots_chat_input")
        if prompt:
            _handle_user_message(prompt, user)
            st.rerun()
    panel.markdown(f'<style>{panel_css}</style>', unsafe_allow_html=True)


def _handle_user_message(prompt: str, user: dict) -> None:
    history = st.session_state.chat_history
    # display-only history (string content) is what we render; the agent gets it too
    display_history = [m for m in history if isinstance(m.get("content"), str)]
    # convert to anthropic-shaped messages
    anth_history = [{"role": m["role"], "content": m["content"]} for m in display_history]

    result = run_turn(prompt, history=anth_history, user=user)
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    st.session_state.chat_history.append({"role": "assistant", "content": result["text"]})
    st.session_state.pending_draft = result["draft"]


def _render_draft_confirm(draft: dict, user: dict) -> None:
    if draft["kind"] == "booking_draft":
        st.info(
            f"📌 Confirm booking: **{draft['court_name']}** on {draft['date']} "
            f"{draft['time_start']}–{draft['time_end']} for ฿{draft['total_price']}?"
        )
    elif draft["kind"] == "cancel_draft":
        st.warning(
            f"⚠️ Cancel booking **{draft['txn_id']}** at {draft['court_name']} "
            f"on {draft['date']} {draft['time_start']}?"
        )

    c1, c2 = st.columns(2)
    if c1.button("Confirm", key="zpots_confirm", type="primary"):
        msg = _commit_draft(draft, user)
        st.session_state.chat_history.append({"role": "assistant", "content": msg})
        st.session_state.pending_draft = None
        st.rerun()
    if c2.button("Cancel", key="zpots_decline"):
        st.session_state.chat_history.append(
            {"role": "assistant", "content": "Okay, I won't do that."}
        )
        st.session_state.pending_draft = None
        st.rerun()


def _commit_draft(draft: dict, user: dict) -> str:
    if draft["kind"] == "booking_draft":
        txn = db.create_booking(
            player_id=user["id"], player_name=user["name"],
            court_id=draft["court_id"], court_name=draft["court_name"],
            date_iso=draft["date"], time_start=draft["time_start"],
            time_end=draft["time_end"], duration=draft["duration"],
            total_price=draft["total_price"],
        )
        return f"✅ Booked! Transaction id **{txn}**."
    if draft["kind"] == "cancel_draft":
        ok = db.cancel_booking(draft["booking_id"], player_id=user["id"])
        return "✅ Cancelled." if ok else "❌ Could not cancel that booking."
    return "Nothing to do."
