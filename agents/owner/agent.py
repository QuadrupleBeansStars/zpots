"""Owner agent tool-calling loop (read-only)."""
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
        messages.append({
            "role": "assistant",
            "content": [_block_to_dict(b) for b in response.content],
        })

        if response.stop_reason != "tool_use":
            text = "".join(b.text for b in response.content if b.type == "text")
            return {"text": text.strip(), "history": messages}

        tool_results = []
        for block in response.content:
            if block.type != "tool_use":
                continue
            result = owner_tools.dispatch(block.name, dict(block.input), user_id=user["id"])
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": json.dumps(result, default=str),
            })
        messages.append({"role": "user", "content": tool_results})

    return {"text": "(agent hop limit reached)", "history": messages}


def _block_to_dict(b) -> dict:
    if b.type == "text":
        return {"type": "text", "text": b.text}
    if b.type == "tool_use":
        return {"type": "tool_use", "id": b.id, "name": b.name, "input": b.input}
    return {"type": b.type}
