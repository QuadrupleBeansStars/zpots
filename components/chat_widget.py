"""Floating chat widget. Mounted once from app.py; branches on session flow.

For player flow: draft proposals (booking/cancel) surface inline Confirm/Cancel buttons
that commit via data.database directly. For owner flow: read-only, no buttons.

Uses streamlit-float: each container is positioned via `container.float(css)` AFTER
its contents are written. Calling `st.markdown(<style>...)` directly does NOT bind
the CSS to a specific container and is silently no-op for positioning.
"""
import streamlit as st
from streamlit_float import float_init, float_css_helper

from agents.player.agent import run_turn as player_run_turn
from agents.owner.agent import run_turn as owner_run_turn
from data import database as db


_CONFIGS = {
    "player": {
        "run_turn": player_run_turn,
        "title": "ZPOTS Assistant",
        "supports_drafts": True,
    },
    "owner": {
        "run_turn": owner_run_turn,
        "title": "ZPOTS Owner Assistant",
        "supports_drafts": False,
    },
}


def render_chat() -> None:
    if not st.session_state.get("logged_in"):
        return
    flow = st.session_state.get("flow")
    cfg = _CONFIGS.get(flow)
    if cfg is None:
        return

    user = {
        "id": st.session_state.user_id,
        "name": st.session_state.user_name,
    }

    float_init(theme=True)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
        st.session_state.pending_draft = None
        st.session_state.chat_open = False

    # Floating launcher button bottom-right.
    btn_container = st.container()
    with btn_container:
        if st.button("💬", key="zpots_chat_toggle", help=f"Chat with {cfg['title']}"):
            st.session_state.chat_open = not st.session_state.chat_open
    btn_container.float(float_css_helper(
        width="64px", right="24px", bottom="24px", z_index="9999",
    ))

    if not st.session_state.chat_open:
        return

    # Floating panel above the button.
    panel = st.container()
    with panel:
        st.markdown(f"**{cfg['title']}**")
        for m in st.session_state.chat_history:
            if isinstance(m["content"], str):
                with st.chat_message(m["role"]):
                    st.write(m["content"])

        draft = st.session_state.pending_draft
        if cfg["supports_drafts"] and draft:
            _render_draft_confirm(draft, user)

        prompt = st.chat_input("Ask anything…", key="zpots_chat_input")
        if prompt:
            _handle_user_message(prompt, user, cfg)
            st.rerun()
    panel.float(float_css_helper(
        width="380px", height="540px", right="24px", bottom="96px",
        background="white", border="1px solid #ddd", border_radius="12px",
        shadow=12, z_index="9999",
        css="overflow-y:auto; padding:14px;",
    ))


def _handle_user_message(prompt: str, user: dict, cfg: dict) -> None:
    history = st.session_state.chat_history
    display_history = [m for m in history if isinstance(m.get("content"), str)]
    anth_history = [{"role": m["role"], "content": m["content"]} for m in display_history]

    # Echo the user message immediately so the spinner appears below it.
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.spinner("Thinking…"):
        result = cfg["run_turn"](prompt, history=anth_history, user=user)

    st.session_state.chat_history.append({"role": "assistant", "content": result["text"]})
    if cfg["supports_drafts"]:
        st.session_state.pending_draft = result.get("draft")


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
