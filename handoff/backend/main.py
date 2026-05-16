"""FastAPI skeleton for ZPOTS backend.

Run: uvicorn main:app --reload
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os

from schemas import Court, TimeSlot, PlayerBooking, DistrictDemand
from ai import parse_search_query, generate_ai_insights, generate_court_description

app = FastAPI(title="ZPOTS API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Courts ---------------------------------------------------------------

@app.get("/api/courts", response_model=list[Court])
def list_courts(sport: Optional[str] = None, district: Optional[str] = None):
    # TODO: replace with SQLAlchemy query
    from seed import COURTS
    courts = COURTS
    if sport:
        courts = [c for c in courts if c["sport"].lower() == sport.lower()]
    if district:
        courts = [c for c in courts if district.lower() in c["district"].lower()]
    return courts


@app.get("/api/courts/{court_id}", response_model=Court)
def get_court(court_id: str):
    from seed import COURTS
    for c in COURTS:
        if c["id"] == court_id:
            return c
    raise HTTPException(404, "court not found")


@app.get("/api/courts/{court_id}/slots", response_model=list[TimeSlot])
def court_slots(court_id: str, date: str):
    from seed import get_time_slots
    return get_time_slots(court_id)


# --- AI -------------------------------------------------------------------

class ParseSearchBody(BaseModel):
    query: str

@app.post("/api/ai/parse-search")
def ai_parse_search(body: ParseSearchBody):
    return parse_search_query(body.query)


class InsightsBody(BaseModel):
    weekly_utilization: dict
    district_demand: list
    owner_bookings: list

@app.post("/api/ai/insights")
def ai_insights(body: InsightsBody):
    return {"markdown": generate_ai_insights(body.weekly_utilization, body.district_demand, body.owner_bookings)}


class DescriptionBody(BaseModel):
    name: str
    sport: str
    surface: str
    location: str
    amenities: list[str]

@app.post("/api/ai/court-description")
def ai_description(body: DescriptionBody):
    return {"description": generate_court_description(**body.model_dump())}


# --- Owner analytics ------------------------------------------------------

@app.get("/api/owner/analytics")
def owner_analytics():
    from seed import WEEKLY_UTILIZATION, DISTRICT_DEMAND
    return {"weekly_utilization": WEEKLY_UTILIZATION, "district_demand": DISTRICT_DEMAND}
