from unittest.mock import MagicMock

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def _set_response(mock_openai_client, content: str):
    """Helper: override the conftest mock to return a specific content string."""
    msg = MagicMock(); msg.content = content
    choice = MagicMock(); choice.message = msg
    resp = MagicMock(); resp.choices = [choice]
    mock_openai_client.chat.completions.create.return_value = resp


def test_parse_search_returns_filters(mock_openai_client):
    _set_response(mock_openai_client, '{"sport": "Badminton", "district": "Sukhumvit", "time_of_day": "evening", "max_price": 400}')
    r = client.post("/ai/parse-search", json={"query": "badminton near Sukhumvit Friday evening under 400 baht"})
    assert r.status_code == 200
    body = r.json()
    assert body["sport"] == "Badminton"
    assert body["district"] == "Sukhumvit"
    assert body["time_of_day"] == "evening"
    assert body["max_price"] == 400


def test_parse_search_returns_nulls_on_garbled_response(mock_openai_client):
    _set_response(mock_openai_client, "not json at all")
    r = client.post("/ai/parse-search", json={"query": "anything"})
    assert r.status_code == 200
    body = r.json()
    assert body == {"sport": None, "district": None, "time_of_day": None, "max_price": None}


def test_parse_search_validates_empty_query():
    r = client.post("/ai/parse-search", json={"query": ""})
    assert r.status_code == 422


def test_insights_returns_markdown(mock_openai_client):
    _set_response(mock_openai_client, "**Friday peaks** drive 41% of revenue.")
    r = client.post("/ai/insights", json={
        "weekly_utilization": {"Mon": 65, "Fri": 91},
        "district_demand": [{"name": "Sukhumvit", "demand": 94, "level": "Peak"}],
        "owner_bookings": [{"customer": "Alex", "sport": "Padel", "status": "CONFIRMED"}],
    })
    assert r.status_code == 200
    assert "Friday peaks" in r.json()["markdown"]


def test_court_description_returns_text(mock_openai_client):
    _set_response(mock_openai_client, "A premium climate-controlled badminton venue.")
    r = client.post("/ai/court-description", json={
        "name": "BBC", "sport": "Badminton", "surface": "Synthetic",
        "location": "Sukhumvit", "amenities": ["AC", "Parking"],
    })
    assert r.status_code == 200
    assert "premium" in r.json()["description"].lower()
