import json
import os
import tempfile
from unittest.mock import patch, MagicMock

import pytest

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


def _completion(finish_reason: str, *, content: str | None = None, tool_calls=None):
    """Build a fake openai.ChatCompletion-shaped object."""
    response = MagicMock()
    choice = MagicMock()
    choice.finish_reason = finish_reason
    choice.message.content = content
    choice.message.tool_calls = tool_calls
    response.choices = [choice]
    return response


def _tool_call(name: str, args: dict, tool_id: str = "t1"):
    tc = MagicMock()
    tc.id = tool_id
    tc.function.name = name
    tc.function.arguments = json.dumps(args)
    return tc


def test_run_turn_returns_text_when_no_tool_use():
    with patch("agents.player.agent.chat") as mock_chat:
        mock_chat.return_value = _completion("stop", content="Hi Alex!")
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
        _completion("tool_calls", tool_calls=[_tool_call("search_courts", {"sport": "Badminton"})]),
        _completion("stop", content="Found Bangkok Badminton Center."),
    ]
    with patch("agents.player.agent.chat", side_effect=responses) as mock_chat:
        result = agent.run_turn("find badminton", history=[], user=user)
    assert "Bangkok Badminton" in result["text"]
    assert mock_chat.call_count == 2


def test_run_turn_surfaces_booking_draft():
    user = {"id": 1, "name": "Alex"}
    responses = [
        _completion("tool_calls", tool_calls=[_tool_call(
            "propose_booking",
            {"court_id": "bbc-01", "date_iso": "2026-06-01",
             "time_start": "18:00", "duration": 1},
        )]),
        _completion("stop", content="Confirm to book."),
    ]
    with patch("agents.player.agent.chat", side_effect=responses):
        result = agent.run_turn("book bbc-01 sat 6pm", history=[], user=user)
    assert result["draft"] is not None
    assert result["draft"]["kind"] == "booking_draft"
