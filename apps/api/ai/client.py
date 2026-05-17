"""Thin LLM client wrapper. Single SDK boundary for the FastAPI service.

Provider is chosen by env var `OPENAI_PROVIDER` (default "azure"). Secrets and
deployment ids are loaded from the project's dev.env via python-dotenv in dev;
Cloud Run injects them as env vars in production.
"""
import logging
import os

from dotenv import load_dotenv
from openai import AzureOpenAI, OpenAI

# client.py lives at apps/api/ai/client.py — 4 dirnames to reach the repo root.
_ENV_PATH = os.path.join(
    os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ),
    "dev.env",
)
load_dotenv(_ENV_PATH)

MAX_TOKENS = 2048

_log = logging.getLogger(__name__)
_client: AzureOpenAI | OpenAI | None = None


def _resolve_model() -> str:
    explicit = os.getenv("ZPOTS_AGENT_MODEL") or os.getenv("AZURE_DEPLOYMENT")
    if explicit:
        return explicit
    provider = os.getenv("OPENAI_PROVIDER", "azure").lower()
    if provider == "azure":
        raise RuntimeError(
            "Azure deployment name is required. Set AZURE_DEPLOYMENT (or "
            "ZPOTS_AGENT_MODEL) in dev.env to your Azure OpenAI deployment name."
        )
    return "gpt-4o-mini"


def _build_client() -> AzureOpenAI | OpenAI:
    provider = os.getenv("OPENAI_PROVIDER", "azure").lower()
    if provider == "azure":
        missing = [
            name for name in ("AZURE_OPENAI_API_KEY", "AZURE_API_VERSION", "AZURE_ENDPOINT")
            if not os.getenv(name)
        ]
        if missing:
            raise RuntimeError(
                f"Azure OpenAI is missing env vars: {', '.join(missing)}. "
                f"Set them in dev.env."
            )
        return AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_API_VERSION"),
            azure_endpoint=os.getenv("AZURE_ENDPOINT"),
        )
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is not set.")
    return OpenAI()


def _get_client() -> AzureOpenAI | OpenAI:
    global _client
    if _client is None:
        _client = _build_client()
    return _client


def _model() -> str:
    return _resolve_model()


def complete(
    user_prompt: str,
    system: str | None = None,
    max_tokens: int = 512,
    json_mode: bool = False,
) -> str:
    """One-shot text generation. Raises on API errors."""
    messages: list[dict] = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": user_prompt})
    kwargs: dict = {"model": _model(), "messages": messages, "max_tokens": max_tokens}
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}
    response = _get_client().chat.completions.create(**kwargs)
    return (response.choices[0].message.content or "").strip()


def chat_completion(
    messages: list[dict],
    system: str,
    max_tokens: int = 512,
) -> str:
    """Multi-turn text completion without tools. Raises on API errors."""
    api_messages: list[dict] = [{"role": "system", "content": system}]
    api_messages.extend({"role": m["role"], "content": m["content"]} for m in messages)
    response = _get_client().chat.completions.create(
        model=_model(),
        messages=api_messages,
        max_tokens=max_tokens,
    )
    return (response.choices[0].message.content or "").strip()
