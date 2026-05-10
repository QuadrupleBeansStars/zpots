from unittest.mock import patch, MagicMock
from agents.owner import agent


def _msg(stop_reason, content):
    m = MagicMock(); m.stop_reason = stop_reason; m.content = content
    return m

def _text(text):
    b = MagicMock(); b.type = "text"; b.text = text
    return b

def _tool(name, args, tool_id="t1"):
    b = MagicMock(); b.type = "tool_use"; b.name = name; b.input = args; b.id = tool_id
    return b


def test_run_turn_returns_text_when_no_tool_use():
    with patch("agents.owner.agent.chat") as mock_chat:
        mock_chat.return_value = _msg("end_turn", [_text("Revenue this week is ฿12,300.")])
        out = agent.run_turn("revenue this week", history=[], user={"id": 3, "name": "Owner"})
    assert "12,300" in out["text"]


def test_run_turn_calls_tool_then_responds():
    user = {"id": 3, "name": "Owner"}
    responses = [
        _msg("tool_use", [_tool("summarize_courts", {})]),
        _msg("end_turn", [_text("You operate 4 courts.")]),
    ]
    with patch("agents.owner.agent.chat", side_effect=responses) as mock_chat:
        out = agent.run_turn("how many courts do I have?", history=[], user=user)
    assert "4 courts" in out["text"]
    assert mock_chat.call_count == 2
