"""Thin LLM client wrapper. Single swap point for model + provider.

Provider is chosen by env var `OPENAI_PROVIDER` (default "azure"). Secrets and
deployment ids are loaded from the project's dev.env via python-dotenv.
"""
import os
from typing import Union

from dotenv import load_dotenv
from openai import AzureOpenAI, OpenAI

# Load secrets from dev.env at the project root if present.
_ENV_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dev.env"
)
load_dotenv(_ENV_PATH)

MODEL = os.getenv("ZPOTS_AGENT_MODEL", os.getenv("AZURE_DEPLOYMENT", "gpt-4o-mini"))
MAX_TOKENS = 2048

_client: Union[AzureOpenAI, OpenAI, None] = None


def _get_client() -> Union[AzureOpenAI, OpenAI]:
    global _client
    if _client is not None:
        return _client
    provider = os.getenv("OPENAI_PROVIDER", "azure").lower()
    if provider == "azure":
        _client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_API_VERSION"),
            azure_endpoint=os.getenv("AZURE_ENDPOINT"),
        )
    else:
        _client = OpenAI()  # reads OPENAI_API_KEY
    return _client


def chat(messages: list[dict], tools: list[dict], system: str):
    """Single turn against the model. Returns the raw OpenAI ChatCompletion object.

    `messages` is the running conversation (user/assistant/tool turns). `system`
    is prepended as the first system message. `tools` is OpenAI tool schema
    (`[{"type": "function", "function": {...}}, ...]`).
    """
    full = [{"role": "system", "content": system}] + list(messages)
    return _get_client().chat.completions.create(
        model=MODEL,
        messages=full,
        tools=tools or None,
        max_tokens=MAX_TOKENS,
    )
