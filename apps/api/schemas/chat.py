"""Chat request / response schemas. Used by /chat/player and /chat/owner."""
from typing import Literal

from pydantic import BaseModel


class ChatUser(BaseModel):
    id: int
    name: str


class ChatMessage(BaseModel):
    role: Literal['user', 'assistant', 'tool', 'system']
    content: str | None = None
    tool_calls: list[dict] | None = None
    tool_call_id: str | None = None


class BookingDraft(BaseModel):
    kind: Literal['booking_draft'] = 'booking_draft'
    court_id: str
    court_name: str
    date: str
    time_start: str
    time_end: str
    duration: int
    total_price: int


class CancelDraft(BaseModel):
    kind: Literal['cancel_draft'] = 'cancel_draft'
    txn_id: str
    court_name: str
    date: str
    time_start: str


class ChatPlayerRequest(BaseModel):
    messages: list[ChatMessage]
    user: ChatUser


class ChatPlayerResponse(BaseModel):
    text: str
    draft: BookingDraft | CancelDraft | None = None
    history: list[ChatMessage]


class ChatOwnerRequest(BaseModel):
    messages: list[ChatMessage]
    user: ChatUser


class ChatOwnerResponse(BaseModel):
    text: str
    history: list[ChatMessage]
