"""Tests for utils/gemini.py — the LLM helper functions used by player/owner pages.

These mock `agents.llm_client.complete` (and the underlying client for the multi-turn
chat helper) so the suite never makes real API calls.
"""
from unittest.mock import patch, MagicMock

from utils import gemini


def test_parse_search_query_handles_plain_json():
    with patch("utils.gemini.complete", return_value='{"sport": "Badminton", "district": null, "time_of_day": "evening", "max_price": 500}'):
        out = gemini.parse_search_query("badminton tonight under 500")
    assert out == {"sport": "Badminton", "district": None, "time_of_day": "evening", "max_price": 500}


def test_parse_search_query_strips_markdown_code_fence():
    fenced = '```json\n{"sport": "Football", "district": "Sukhumvit", "time_of_day": null, "max_price": null}\n```'
    with patch("utils.gemini.complete", return_value=fenced):
        out = gemini.parse_search_query("football in sukhumvit")
    assert out["sport"] == "Football"
    assert out["district"] == "Sukhumvit"


def test_parse_search_query_returns_empty_filters_on_error():
    with patch("utils.gemini.complete", side_effect=RuntimeError("api down")):
        out = gemini.parse_search_query("anything")
    assert out == {"sport": None, "district": None, "time_of_day": None, "max_price": None}


def test_generate_court_description_returns_model_text():
    with patch("utils.gemini.complete", return_value="A premium climate-controlled badminton venue in the heart of Sukhumvit."):
        out = gemini.generate_court_description(
            name="BBC", sport="Badminton", surface="Synthetic",
            location="Pathum Wan", amenities=["AC", "Parking"],
        )
    assert "Sukhumvit" in out


def test_generate_court_description_falls_back_on_error():
    with patch("utils.gemini.complete", side_effect=RuntimeError("boom")):
        out = gemini.generate_court_description(
            name="BBC", sport="Badminton", surface="x", location="y", amenities=[],
        )
    assert "Unable to generate description" in out


def test_chat_with_court_assistant_uses_history_and_system():
    fake_response = MagicMock()
    fake_response.choices = [MagicMock()]
    fake_response.choices[0].message.content = "BTS Asok is the closest stop."
    fake_client = MagicMock()
    fake_client.chat.completions.create.return_value = fake_response

    court = {"name": "BBC", "sport": "Badminton", "amenities": [{"value": "AC"}]}
    booking = {"date": "2026-06-01", "time_start": "18:00", "time_end": "19:00"}

    with patch("agents.llm_client._get_client", return_value=fake_client):
        out = gemini.chat_with_court_assistant(
            messages=[{"role": "user", "content": "how do I get there?"}],
            court=court, booking=booking,
        )

    assert "BTS Asok" in out
    sent = fake_client.chat.completions.create.call_args.kwargs["messages"]
    assert sent[0]["role"] == "system"
    assert "ZPOTS" in sent[0]["content"]
    assert sent[1] == {"role": "user", "content": "how do I get there?"}
