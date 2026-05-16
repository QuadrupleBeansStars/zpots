"""Pydantic schemas mirroring data/dummy_data.py shapes.

Kept deliberately close to the existing Python dicts so the migration is mechanical.
"""
from pydantic import BaseModel
from typing import Optional


class Amenity(BaseModel):
    icon: str
    label: str
    value: str


class CourtUnit(BaseModel):
    number: str
    surface: str


class Court(BaseModel):
    id: str
    name: str
    short_name: str
    sport: str
    rating: float
    reviews: int
    location: str
    address: str
    district: str
    price_per_hour: int
    prime_price: int
    amenities: list[Amenity]
    surface: str
    status: str
    utilization: int
    peak_hours: str
    ai_efficiency: str
    tags: list[str]
    color: str
    courts: list[CourtUnit]


class TimeSlot(BaseModel):
    time_start: str
    time_end: str
    price: int
    status: str
    ai_tag: Optional[str] = None


class PlayerBooking(BaseModel):
    id: str
    court_id: str
    court_name: str
    time_start: str
    time_end: str
    status: str
    total: int


class DistrictDemand(BaseModel):
    name: str
    demand: int
    level: str
