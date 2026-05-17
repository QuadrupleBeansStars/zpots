from unittest.mock import MagicMock

from agents.owner import agent


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


def test_run_turn_returns_text_when_no_tool_calls(mock_openai_client):
    mock_openai_client.chat.completions.create.return_value = _msg(content="Hi Owner")
    result = agent.run_turn(
        messages=[{"role": "user", "content": "hello"}],
        user={"id": 3, "name": "Venue Admin"},
    )
    assert result["text"] == "Hi Owner"
    assert "history" in result


def test_run_turn_dispatches_summarize_courts(mock_openai_client):
    mock_openai_client.chat.completions.create.side_effect = [
        _msg(tool_calls=[_tool_call("summarize_courts", "{}")]),
        _msg(content="You operate 6 courts across Bangkok."),
    ]
    result = agent.run_turn(
        messages=[{"role": "user", "content": "how many courts?"}],
        user={"id": 3, "name": "Venue Admin"},
    )
    assert "6 courts" in result["text"]
    assert mock_openai_client.chat.completions.create.call_count == 2
