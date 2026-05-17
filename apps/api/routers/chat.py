from fastapi import APIRouter

from agents.player.agent import run_turn as player_run_turn
from agents.owner.agent import run_turn as owner_run_turn
from schemas.chat import (
    ChatOwnerRequest, ChatOwnerResponse,
    ChatPlayerRequest, ChatPlayerResponse,
)

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/player", response_model=ChatPlayerResponse)
def chat_player(req: ChatPlayerRequest) -> ChatPlayerResponse:
    result = player_run_turn(
        messages=[m.model_dump(exclude_none=True) for m in req.messages],
        user=req.user.model_dump(),
        bookings=[b.model_dump() for b in req.bookings],
    )
    return ChatPlayerResponse(
        text=result["text"],
        draft=result["draft"],
        history=result["history"],
    )


@router.post("/owner", response_model=ChatOwnerResponse)
def chat_owner(req: ChatOwnerRequest) -> ChatOwnerResponse:
    result = owner_run_turn(
        messages=[m.model_dump(exclude_none=True) for m in req.messages],
        user=req.user.model_dump(),
    )
    return ChatOwnerResponse(
        text=result["text"],
        history=result["history"],
    )
