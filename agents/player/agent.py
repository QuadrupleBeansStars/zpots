"""Player agent tool-calling loop."""
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
        # Append the assistant turn (including tool_use blocks) verbatim.
        messages.append({
            "role": "assistant",
            "content": [_block_to_dict(b) for b in response.content],
        })

        if response.stop_reason != "tool_use":
            text = "".join(b.text for b in response.content if b.type == "text")
            return {"text": text.strip(), "draft": pending_draft, "history": messages}

        tool_results = []
        for block in response.content:
            if block.type != "tool_use":
                continue
            result = player_tools.dispatch(block.name, dict(block.input), user_id=user["id"])
            if isinstance(result, dict) and result.get("kind") in ("booking_draft", "cancel_draft"):
                pending_draft = result
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": _stringify(result),
            })
        messages.append({"role": "user", "content": tool_results})

    return {"text": "(agent hop limit reached)", "draft": pending_draft, "history": messages}


def _block_to_dict(b) -> dict:
    if b.type == "text":
        return {"type": "text", "text": b.text}
    if b.type == "tool_use":
        return {"type": "tool_use", "id": b.id, "name": b.name, "input": b.input}
    return {"type": b.type}


def _stringify(v) -> str:
    import json
    return json.dumps(v, default=str)
