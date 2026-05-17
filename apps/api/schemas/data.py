"""Pydantic schemas for /courts and /bookings endpoints.

Court keeps the rich frontend shape so a single response satisfies both
frontend pages and agent tools (agents ignore the extra fields).
"""
from typing import Literal

from pydantic import BaseModel


class Amenity(BaseModel):
    icon: str
    label: str
    value: str


class CourtSubCourt(BaseModel):
    number: str
    surface: str


class Court(BaseModel):
    id: str
    name: str
    short_name: str | None = None
    sport: str
    rating: float | None = None
    reviews: int | None = None
    location: str | None = None
    address: str | None = None
    district: str
    price_per_hour: int
    prime_price: int | None = None
    amenities: list[Amenity] = []
    surface: str | None = None
    status: Literal["ACTIVE", "INACTIVE"] | None = "ACTIVE"
    utilization: int | None = None
    utilization_pct: int | None = None
    peak_hours: str | None = None
    ai_efficiency: str | None = None
    tags: list[str] = []
    color: str | None = None
    courts: list[CourtSubCourt] = []


class Booking(BaseModel):
    txn_id: str
    user_id: int
    player_name: str
    court_id: str
    court_name: str
    date: str
    time_start: str
    time_end: str
    duration: int
    total_price: int
    status: Literal["CONFIRMED", "CANCELLED"]


class CreateBookingRequest(BaseModel):
    user_id: int
    court_id: str
    date: str
    time_start: str
    duration: int
    player_name: str | None = None
