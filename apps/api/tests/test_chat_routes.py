from unittest.mock import MagicMock

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def _msg(content: str | None = None, tool_calls: list | None = None):
    msg = MagicMock(); msg.content = content; msg.tool_calls = tool_calls
    choice = MagicMock(); choice.message = msg
    choice.finish_reason = "tool_calls" if tool_calls else "stop"
    resp = MagicMock(); resp.choices = [choice]
    return resp


def test_chat_player_returns_text_and_history(mock_openai_client):
    mock_openai_client.chat.completions.create.return_value = _msg(content="Hi Alex!")
    r = client.post("/chat/player", json={
        "messages": [{"role": "user", "content": "hello"}],
        "user": {"id": 1, "name": "Alex"},
    })
    assert r.status_code == 200
    body = r.json()
    assert body["text"] == "Hi Alex!"
    assert body["draft"] is None
    assert len(body["history"]) >= 2


def test_chat_owner_returns_text_and_history(mock_openai_client):
    mock_openai_client.chat.completions.create.return_value = _msg(content="Revenue today: ฿1,420.")
    r = client.post("/chat/owner", json={
        "messages": [{"role": "user", "content": "revenue?"}],
        "user": {"id": 3, "name": "Venue Admin"},
    })
    assert r.status_code == 200
    body = r.json()
    assert "1,420" in body["text"]
    assert "draft" not in body
