"""Tests for utils/gemini.py — the LLM helper functions used by player/owner pages.

These mock `agents.llm_client.complete` (and the underlying client for the multi-turn
chat helper) so the suite never makes real API calls.
"""
from unittest.mock import patch, MagicMock

from utils import gemini


def test_parse_search_query_handles_plain_json():
    with patch("utils.gemini.complete", return_value='{"sport": "Badminton", "district": null, "time_of_day": "evening", "max_price": 500}') as m:
        out = gemini.parse_search_query("badminton tonight under 500")
    assert out == {"sport": "Badminton", "district": None, "time_of_day": "evening", "max_price": 500}
    # JSON mode must be requested so the model never wraps the response in markdown.
    assert m.call_args.kwargs["json_mode"] is True


def test_parse_search_query_returns_empty_filters_on_invalid_json():
    with patch("utils.gemini.complete", return_value="not json at all"):
        out = gemini.parse_search_query("garbled response")
    assert out == {"sport": None, "district": None, "time_of_day": None, "max_price": None}


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
    court = {"name": "BBC", "sport": "Badminton", "amenities": [{"value": "AC"}]}
    booking = {"date": "2026-06-01", "time_start": "18:00", "time_end": "19:00"}
    captured = {}

    def fake_chat_completion(messages, system, max_tokens=512):
        captured["messages"] = messages
        captured["system"] = system
        return "BTS Asok is the closest stop."

    with patch("utils.gemini.chat_completion", side_effect=fake_chat_completion):
        out = gemini.chat_with_court_assistant(
            messages=[{"role": "user", "content": "how do I get there?"}],
            court=court, booking=booking,
        )

    assert "BTS Asok" in out
    assert "ZPOTS" in captured["system"]
    assert captured["messages"] == [{"role": "user", "content": "how do I get there?"}]


def test_chat_with_court_assistant_falls_back_on_error():
    court = {"name": "BBC", "sport": "Badminton", "amenities": []}
    booking = {"date": "2026-06-01", "time_start": "18:00", "time_end": "19:00"}
    with patch("utils.gemini.chat_completion", side_effect=RuntimeError("api down")):
        out = gemini.chat_with_court_assistant(
            messages=[{"role": "user", "content": "anything"}],
            court=court, booking=booking,
        )
    assert "couldn't process" in out.lower()
