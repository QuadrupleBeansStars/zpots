"""Player agent tool-calling loop (OpenAI / Azure OpenAI)."""
import json

from agents.llm_client import chat
from agents.player import tools as player_tools
from agents.player.system_prompt import build_system_prompt

MAX_HOPS = 6  # safety cap so the model can't loop forever


def run_turn(user_message: str, history: list[dict], user: dict) -> dict:
    """Run one user turn through the agent. Returns:
        {"text": <final assistant text>, "draft": <pending draft dict or None>,
         "history": <updated message history to store in session>}
    """
    messages = list(history) + [{"role": "user", "content": user_message}]
    system = build_system_prompt(user)
    pending_draft = None

    for _ in range(MAX_HOPS):
        response = chat(messages, tools=player_tools.TOOLS, system=system)
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
            return {
                "text": (msg.content or "").strip(),
                "draft": pending_draft,
                "history": messages,
            }

        for tc in msg.tool_calls or []:
            try:
                args = json.loads(tc.function.arguments or "{}")
            except json.JSONDecodeError:
                args = {}
            result = player_tools.dispatch(tc.function.name, args, user_id=user["id"])
            if isinstance(result, dict) and result.get("kind") in ("booking_draft", "cancel_draft"):
                pending_draft = result
            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": json.dumps(result, default=str),
            })

    return {"text": "(agent hop limit reached)", "draft": pending_draft, "history": messages}
