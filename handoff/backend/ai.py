"""Gemini AI helpers — ported from legacy/utils/gemini.py.

Changes from the Streamlit original:
1. `st.secrets["GEMINI_API_KEY"]` → `os.environ["GEMINI_API_KEY"]`
2. Model name fixed to a real stable model (was "gemini-3-flash-preview" which doesn't exist).
3. No streamlit import.
"""
import json
import os
from google import genai
from google.genai import types

_client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
_MODEL = "gemini-2.5-flash"

SPORTS_LIST = ["Badminton", "Football", "Basketball", "Padel"]
DISTRICTS = ["Sukhumvit", "Thong Lor", "Ari", "Pathumwan", "Silom"]


def parse_search_query(query: str) -> dict:
    prompt = f"""Extract sports court search filters from this query and return ONLY valid JSON.

Query: "{query}"

Return JSON with exactly these keys (use null if not mentioned):
- "sport": one of {SPORTS_LIST} or null
- "district": one of {DISTRICTS} or null
- "time_of_day": one of ["morning", "afternoon", "evening"] or null
- "max_price": integer (baht per hour) or null

Return ONLY the JSON object."""
    try:
        response = _client.models.generate_content(model=_MODEL, contents=prompt)
        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        return json.loads(text.strip())
    except Exception:
        return {"sport": None, "district": None, "time_of_day": None, "max_price": None}


def generate_ai_insights(weekly_util: dict, district_demand: list, owner_bookings: list) -> str:
    booking_summary = ", ".join(
        f"{b['customer']} ({b['sport']} - {b['status']})" for b in owner_bookings
    )
    util_str = ", ".join(f"{day}: {pct}%" for day, pct in weekly_util.items())
    demand_str = ", ".join(f"{d['name']}: {d['demand']}% ({d['level']})" for d in district_demand)

    prompt = f"""You are an AI analytics expert for ZPOTS, a Bangkok sports court booking platform.

Data:
- Weekly utilization: {util_str}
- District demand: {demand_str}
- Recent bookings: {booking_summary}

Generate a concise venue performance summary (3–4 short paragraphs) covering:
1. Peak performance days/times and demand drivers
2. No-show risk assessment
3. Two or three actionable pricing/scheduling recommendations

Use markdown with **bold** for key numbers. Keep under 200 words."""
    try:
        response = _client.models.generate_content(model=_MODEL, contents=prompt)
        return response.text
    except Exception as e:
        return f"Unable to generate insights. ({e})"


def generate_court_description(name: str, sport: str, surface: str, location: str, amenities: list) -> str:
    amenities_str = ", ".join(amenities) if amenities else "standard facilities"
    prompt = f"""Write a compelling 2–3 sentence listing description for a Bangkok sports court.

Name: {name}
Sport: {sport}
Surface: {surface}
Location: {location}
Amenities: {amenities_str}

Tone: professional, energetic. Output ONLY the description."""
    try:
        response = _client.models.generate_content(model=_MODEL, contents=prompt)
        return response.text.strip()
    except Exception as e:
        return f"Unable to generate description. ({e})"
