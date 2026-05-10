import os
import tempfile
import pytest
from unittest.mock import patch, MagicMock
from data import database as db
from agents.player import agent


@pytest.fixture(autouse=True)
def fresh_db(monkeypatch):
    """Provide an isolated SQLite DB for each test that hits real tool dispatch."""
    tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    tmp.close()
    monkeypatch.setattr(db, "DB_PATH", tmp.name)
    db.get_connection.clear()
    db.init_db()
    yield
    os.unlink(tmp.name)


def _msg(stop_reason, content):
    m = MagicMock()
    m.stop_reason = stop_reason
    m.content = content
    return m


def _text_block(text):
    b = MagicMock(); b.type = "text"; b.text = text
    return b


def _tool_block(name, args, tool_id="t1"):
    b = MagicMock(); b.type = "tool_use"; b.name = name; b.input = args; b.id = tool_id
    return b


def test_run_turn_returns_text_when_no_tool_use():
    with patch("agents.player.agent.chat") as mock_chat:
        mock_chat.return_value = _msg("end_turn", [_text_block("Hi Alex!")])
        result = agent.run_turn(
            "hello",
            history=[],
            user={"id": 1, "name": "Alex"},
        )
    assert result["text"] == "Hi Alex!"
    assert result["draft"] is None


def test_run_turn_dispatches_tool_then_responds():
    user = {"id": 1, "name": "Alex"}
    responses = [
        _msg("tool_use", [_tool_block("search_courts", {"sport": "Badminton"})]),
        _msg("end_turn", [_text_block("Found Bangkok Badminton Center.")]),
    ]
    with patch("agents.player.agent.chat", side_effect=responses) as mock_chat:
        result = agent.run_turn("find badminton", history=[], user=user)
    assert "Bangkok Badminton" in result["text"]
    assert mock_chat.call_count == 2


def test_run_turn_surfaces_booking_draft():
    user = {"id": 1, "name": "Alex"}
    responses = [
        _msg("tool_use", [_tool_block(
            "propose_booking",
            {"court_id": "bbc-01", "date_iso": "2026-06-01",
             "time_start": "18:00", "duration": 1},
        )]),
        _msg("end_turn", [_text_block("Confirm to book.")]),
    ]
    with patch("agents.player.agent.chat", side_effect=responses):
        result = agent.run_turn("book bbc-01 sat 6pm", history=[], user=user)
    assert result["draft"] is not None
    assert result["draft"]["kind"] == "booking_draft"
