import json
from unittest.mock import patch, MagicMock

from agents.owner import agent


def _completion(finish_reason: str, *, content: str | None = None, tool_calls=None):
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
    with patch("agents.owner.agent.chat") as mock_chat:
        mock_chat.return_value = _completion("stop", content="Revenue this week is ฿12,300.")
        out = agent.run_turn("revenue this week", history=[], user={"id": 3, "name": "Owner"})
    assert "12,300" in out["text"]


def test_run_turn_calls_tool_then_responds():
    user = {"id": 3, "name": "Owner"}
    responses = [
        _completion("tool_calls", tool_calls=[_tool_call("summarize_courts", {})]),
        _completion("stop", content="You operate 4 courts."),
    ]
    with patch("agents.owner.agent.chat", side_effect=responses) as mock_chat:
        out = agent.run_turn("how many courts do I have?", history=[], user=user)
    assert "4 courts" in out["text"]
    assert mock_chat.call_count == 2
