"""Pytest configuration and autouse fixtures.

- Adds apps/api/ to sys.path so tests can `from main import app` etc.
- Mocks ai.client._get_client() so tests never hit Azure OpenAI.
"""
import os
import sys
from unittest.mock import MagicMock

import pytest

# Ensure apps/api/ is on sys.path so test imports of `main`, `ai.*`, etc. resolve.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture(autouse=True)
def mock_openai_client(monkeypatch):
    """Replace ai.client._get_client() with a MagicMock that returns canned responses.

    Tests that need a specific response payload override
    `fake_client.chat.completions.create.return_value` via the returned mock.
    """
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
