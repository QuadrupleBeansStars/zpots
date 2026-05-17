"""Pytest configuration and autouse fixtures.

- Adds apps/api/ to sys.path so tests can `from main import app` etc.
- Mocks ai.client._get_client() so tests never hit Azure OpenAI.
- Freezes seed_loader._today() to a deterministic date.
- Reinitializes the in-memory stores before every test.
"""
import os
import sys
from datetime import date
from unittest.mock import MagicMock

import pytest

# Ensure apps/api/ is on sys.path so test imports of `main`, `ai.*`, etc. resolve.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

FROZEN_TODAY = date(2099, 1, 1)


@pytest.fixture(autouse=True)
def freeze_today_and_reset_stores(monkeypatch):
    """Freeze 'today' and rebuild the in-memory stores before each test.

    Without this, tests depending on dates would be flaky as days pass,
    and tests that mutate the BookingsStore would bleed state into each
    other.
    """
    from data import seed_loader, store

    monkeypatch.setattr(seed_loader, "_today", lambda: FROZEN_TODAY)
    store.init_stores()
    yield


@pytest.fixture(autouse=True)
def mock_openai_client(monkeypatch):
    """Replace ai.client._get_client() with a MagicMock that returns canned responses."""
    fake_msg = MagicMock()
    fake_msg.content = '{"sport": null, "district": null, "time_of_day": null, "max_price": null}'
    fake_choice = MagicMock()
    fake_choice.message = fake_msg
    fake_response = MagicMock()
    fake_response.choices = [fake_choice]
    fake_client = MagicMock()
    fake_client.chat.completions.create.return_value = fake_response
    monkeypatch.setattr("ai.client._get_client", lambda: fake_client)
    monkeypatch.setattr("ai.client._model", lambda: "test-deployment")
    return fake_client
