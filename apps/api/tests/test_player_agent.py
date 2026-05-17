from unittest.mock import MagicMock

from agents.player import agent


def _msg(content: str | None = None, tool_calls: list | None = None):
    msg = MagicMock(); msg.content = content; msg.tool_calls = tool_calls
    choice = MagicMock(); choice.message = msg
    choice.finish_reason = "tool_calls" if tool_calls else "stop"
    resp = MagicMock(); resp.choices = [choice]
    return resp


def _tool_call(name: str, args: str = "{}", tc_id: str = "t1"):
    tc = MagicMock(); tc.id = tc_id
    tc.function.name = name
    tc.function.arguments = args
    return tc


def test_run_turn_returns_text_when_no_tool_calls(monkeypatch, mock_openai_client):
    fake = mock_openai_client
    fake.chat.completions.create.return_value = _msg(content="Hi Alex!")

    result = agent.run_turn(
        messages=[{"role": "user", "content": "hello"}],
        user={"id": 1, "name": "Alex"},
        bookings=[],
    )

    assert result["text"] == "Hi Alex!"
    assert result["draft"] is None
    assert len(result["history"]) == 2  # user + assistant


def test_run_turn_dispatches_tool_then_responds(monkeypatch, mock_openai_client):
    fake = mock_openai_client
    fake.chat.completions.create.side_effect = [
        _msg(tool_calls=[_tool_call("search_courts", '{"sport": "Badminton"}')]),
        _msg(content="Found Bangkok Badminton Center."),
    ]

    result = agent.run_turn(
        messages=[{"role": "user", "content": "find badminton"}],
        user={"id": 1, "name": "Alex"},
        bookings=[],
    )

    assert "Bangkok Badminton" in result["text"]
    assert fake.chat.completions.create.call_count == 2


def test_run_turn_surfaces_booking_draft(monkeypatch, mock_openai_client):
    fake = mock_openai_client
    fake.chat.completions.create.side_effect = [
        _msg(tool_calls=[_tool_call(
            "propose_booking",
            '{"court_id": "bbc-01", "date_iso": "2099-06-01", "time_start": "18:00", "duration": 1}',
        )]),
        _msg(content="Confirm to book?"),
    ]

    result = agent.run_turn(
        messages=[{"role": "user", "content": "book bbc-01 tomorrow 6pm"}],
        user={"id": 1, "name": "Alex"},
        bookings=[],
    )

    assert result["draft"] is not None
    assert result["draft"]["kind"] == "booking_draft"
    assert result["draft"]["court_name"] == "Bangkok Badminton Center"
