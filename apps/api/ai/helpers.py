"""AI helpers for the FastAPI service. Ported from utils/gemini.py."""
import json
import logging

from ai.client import chat_completion, complete

_log = logging.getLogger(__name__)

SPORTS_LIST = ["Badminton", "Football", "Basketball", "Padel"]
DISTRICTS = ["Sukhumvit", "Thong Lor", "Ari", "Pathumwan", "Silom"]


def parse_search_query(query: str) -> dict:
    """Parse a natural-language court search query into structured filters.

    Returns dict with keys: sport, district, time_of_day, max_price.
    Any unrecognised field is null. Returns all-null on parser failure.
    """
    prompt = f"""Extract sports court search filters from this query and return ONLY valid JSON.

Query: "{query}"

Return JSON with exactly these keys (use null if not mentioned):
- "sport": one of {SPORTS_LIST} or null
- "district": one of {DISTRICTS} or null
- "time_of_day": one of ["morning", "afternoon", "evening"] or null
  (morning = 06:00-12:00, afternoon = 12:00-17:00, evening = 17:00-22:00)
- "max_price": integer (baht per hour) or null"""

    try:
        text = complete(prompt, max_tokens=256, json_mode=True)
        return json.loads(text)
    except Exception:
        _log.exception("parse_search_query failed; returning empty filters")
        return {"sport": None, "district": None, "time_of_day": None, "max_price": None}


def generate_ai_insights(weekly_util: dict, district_demand: list, owner_bookings: list) -> str:
    """Generate natural-language AI insights for a venue owner. Returns markdown."""
    booking_summary = ", ".join(
        f"{b['customer']} ({b['sport']} - {b['status']})" for b in owner_bookings
    )
    util_str = ", ".join(f"{day}: {pct}%" for day, pct in weekly_util.items())
    demand_str = ", ".join(f"{d['name']}: {d['demand']}% ({d['level']})" for d in district_demand)

    prompt = f"""You are an AI analytics expert for ZPOTS, a sports court booking platform in Bangkok, Thailand.

Here is the venue data:
- Weekly utilization: {util_str}
- District demand levels: {demand_str}
- Recent bookings: {booking_summary}

Generate a concise venue performance summary (3–4 short paragraphs) covering:
1. Peak performance days/times and what's driving demand
2. No-show risk assessment with specific risk factors
3. Two or three actionable pricing or scheduling recommendations to increase revenue

Use markdown formatting with **bold** for key numbers. Be specific and data-driven. Keep it under 200 words."""

    try:
        return complete(prompt, max_tokens=512)
    except Exception:
        _log.exception("generate_ai_insights failed")
        return "Unable to generate insights at this time. Please try again."


def generate_court_description(name: str, sport: str, surface: str, location: str, amenities: list) -> str:
    """Generate a compelling court listing description for venue owners."""
    amenities_str = ", ".join(amenities) if amenities else "standard facilities"
    prompt = f"""Write a compelling 2–3 sentence listing description for a sports court in Bangkok.

Court details:
- Name: {name}
- Sport: {sport}
- Surface: {surface}
- Location: {location}
- Amenities: {amenities_str}

Tone: professional, energetic, appealing to Bangkok sports enthusiasts.
Output ONLY the description text — no headings, no quotes, no extra commentary."""

    try:
        return complete(prompt, max_tokens=256)
    except Exception:
        _log.exception("generate_court_description failed")
        return "Unable to generate description at this time."
