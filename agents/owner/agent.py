"""Owner agent tool-calling loop (read-only, OpenAI / Azure OpenAI)."""
import json

from agents.llm_client import chat
from agents.owner import tools as owner_tools
from agents.owner.system_prompt import build_system_prompt

MAX_HOPS = 6


def run_turn(user_message: str, history: list[dict], user: dict) -> dict:
    """Run one user turn. Returns {"text": <final assistant text>, "history": <updated history>}."""
    messages = list(history) + [{"role": "user", "content": user_message}]
    system = build_system_prompt(user)

    for _ in range(MAX_HOPS):
        response = chat(messages, tools=owner_tools.TOOLS, system=system)
        choice = response.choices[0]
        msg = choice.message

        assistant_turn: dict = {"role": "assistant", "content": msg.content or ""}
        if msg.tool_calls:
            assistant_turn["tool_calls"] = [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {"name": tc.function.name, "arguments": tc.function.arguments},
                }
                for tc in msg.tool_calls
            ]
        messages.append(assistant_turn)

        if choice.finish_reason != "tool_calls":
            return {"text": (msg.content or "").strip(), "history": messages}

        for tc in msg.tool_calls or []:
            try:
                args = json.loads(tc.function.arguments or "{}")
            except json.JSONDecodeError:
                args = {}
            result = owner_tools.dispatch(tc.function.name, args, user_id=user["id"])
            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": json.dumps(result, default=str),
            })

    return {"text": "(agent hop limit reached)", "history": messages}
