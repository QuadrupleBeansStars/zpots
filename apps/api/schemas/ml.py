from typing import Literal

from pydantic import BaseModel, Field


class DemandCell(BaseModel):
    court_id: str
    day_of_week: int = Field(..., ge=0, le=6)
    hour: int = Field(..., ge=0, le=23)
    predicted_bookings: float


class DemandForecastResponse(BaseModel):
    cells: list[DemandCell]


class NoShowRiskItem(BaseModel):
    sport: str = "Badminton"
    district: str = "Sukhumvit"
    day_of_week: int = Field(default=2, ge=0, le=6)
    hour: int = Field(default=18, ge=0, le=23)
    is_weekend: bool = False
    is_holiday: bool = False
    weather: str = "sunny"
    price: int = 500
    lead_time_days: int = 3
    is_repeat_customer: bool = True


class NoShowRiskResult(BaseModel):
    tier: Literal["Low", "Medium", "High"]
    probability: float


class NoShowRiskBatchRequest(BaseModel):
    items: list[NoShowRiskItem]


class NoShowRiskBatchResponse(BaseModel):
    results: list[NoShowRiskResult]
