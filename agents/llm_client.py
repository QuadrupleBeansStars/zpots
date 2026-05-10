"""Thin wrapper around the Anthropic SDK so the rest of the agent code is model-agnostic.

The MODEL constant is the single swap point when the new LLM deployment lands.
"""
import os
from anthropic import Anthropic

# TODO: swap to the new deployment id once provided.
MODEL = os.getenv("ZPOTS_AGENT_MODEL", "claude-sonnet-4-6")
MAX_TOKENS = 1024

_client: Anthropic | None = None


def _get_client() -> Anthropic:
    global _client
    if _client is None:
        _client = Anthropic()  # reads ANTHROPIC_API_KEY from env
    return _client


def chat(messages: list[dict], tools: list[dict], system: str):
    """Single turn against the model. Returns the raw Anthropic Message object."""
    return _get_client().messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=system,
        tools=tools,
        messages=messages,
    )
