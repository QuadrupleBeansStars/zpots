"""Gemini AI helpers for ZPOTS."""
import json
from google import genai
from google.genai import types

GEMINI_API_KEY = "AIzaSyAZdZrDSif-yES_xr7dH2R-SUyd4RPCngA"
_client = genai.Client(api_key=GEMINI_API_KEY)
_MODEL = "gemini-3-flash-preview"

SPORTS_LIST = ["Badminton", "Football", "Basketball", "Padel"]
DISTRICTS = ["Sukhumvit", "Thong Lor", "Ari", "Pathumwan", "Silom"]


def parse_search_query(query: str) -> dict:
    """Parse a natural language court search query into structured filters.

    Returns dict with keys: sport, district, time_of_day, max_price.
    Any unrecognised field is null.
    """
    prompt = f"""Extract sports court search filters from this query and return ONLY valid JSON.

Query: "{query}"

Return JSON with exactly these keys (use null if not mentioned):
- "sport": one of {SPORTS_LIST} or null
- "district": one of {DISTRICTS} or null
- "time_of_day": one of ["morning", "afternoon", "evening"] or null
  (morning = 06:00-12:00, afternoon = 12:00-17:00, evening = 17:00-22:00)
- "max_price": integer (baht per hour) or null

Return ONLY the JSON object, no markdown, no explanation."""

    try:
        response = _client.models.generate_content(model=_MODEL, contents=prompt)
        text = response.text.strip()
        # Strip markdown code fences if present
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        return json.loads(text.strip())
    except Exception:
        return {"sport": None, "district": None, "time_of_day": None, "max_price": None}


def generate_ai_insights(weekly_util: dict, district_demand: list, owner_bookings: list) -> str:
    """Generate natural language AI insights for a venue owner.

    Returns a markdown-formatted string with observations and recommendations.
    """
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
        response = _client.models.generate_content(model=_MODEL, contents=prompt)
        return response.text
    except Exception as e:
        return f"Unable to generate insights at this time. Please try again. ({e})"


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
        response = _client.models.generate_content(model=_MODEL, contents=prompt)
        return response.text.strip()
    except Exception as e:
        return f"Unable to generate description at this time. ({e})"


def chat_with_court_assistant(messages: list, court: dict, booking: dict) -> str:
    """Send a chat message with court context and return the assistant reply.

    messages: list of {"role": "user"|"assistant", "content": str}
    """
    amenities_str = ", ".join(a["value"] for a in court.get("amenities", []))
    system_instruction = f"""You are a helpful booking assistant for ZPOTS, a sports court booking platform in Bangkok.

The player has just booked:
- Court: {court['name']}
- Sport: {court['sport']}
- Address: {court.get('address', '')} ({court.get('district', '')} district)
- Surface: {court.get('surface', '')}
- Amenities: {amenities_str}
- Peak hours: {court.get('peak_hours', '')}
- Price: ฿{court.get('price_per_hour', '')} / hour

Booking details:
- Date: {booking.get('date', '')}
- Time: {booking.get('time_start', '')} – {booking.get('time_end', '')}
- Court number: {booking.get('court_number', '')}

Answer questions about directions, transport (BTS/MRT), parking, what to bring, dress code, rules, or anything about the venue. Be concise and friendly."""

    # Build conversation history for the API
    history = []
    for msg in messages[:-1]:
        role = "user" if msg["role"] == "user" else "model"
        history.append(types.Content(role=role, parts=[types.Part(text=msg["content"])]))

    last_user_msg = messages[-1]["content"] if messages else ""

    try:
        chat = _client.chats.create(
            model=_MODEL,
            config=types.GenerateContentConfig(system_instruction=system_instruction),
            history=history,
        )
        response = chat.send_message(last_user_msg)
        return response.text
    except Exception as e:
        return f"Sorry, I couldn't process that right now. Please try again. ({e})"
