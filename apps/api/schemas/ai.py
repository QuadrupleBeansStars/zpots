from typing import Literal

from pydantic import BaseModel, Field


class ParseSearchRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=500)


class ParseSearchResponse(BaseModel):
    sport: str | None = None
    district: str | None = None
    time_of_day: Literal["morning", "afternoon", "evening"] | None = None
    max_price: int | None = None


class InsightsRequest(BaseModel):
    weekly_utilization: dict[str, int]
    district_demand: list[dict]
    owner_bookings: list[dict]


class InsightsResponse(BaseModel):
    markdown: str


class CourtDescriptionRequest(BaseModel):
    name: str
    sport: str
    surface: str
    location: str
    amenities: list[str]


class CourtDescriptionResponse(BaseModel):
    description: str
