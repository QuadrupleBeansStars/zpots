"""All dummy data for the ZPOTS platform."""

COURTS = [
    {
        "id": "bbc-01",
        "name": "Bangkok Badminton Center",
        "short_name": "Bangkok Badminton",
        "sport": "Badminton",
        "rating": 4.8,
        "reviews": 100,
        "location": "Pathum Wan, Bangkok 10330, Thailand",
        "address": "88 Ratchadapisek Rd.",
        "district": "Sukhumvit",
        "price_per_hour": 450,
        "prime_price": 650,
        "amenities": [
            {"icon": "ac_unit", "label": "Climate", "value": "Full AC"},
            {"icon": "local_parking", "label": "Parking", "value": "Free (50+ Slots)"},
            {"icon": "checkroom", "label": "Facilities", "value": "Changing Rooms"},
            {"icon": "water_drop", "label": "Water", "value": "Dispenser"},
        ],
        "surface": "Premium Synthetic",
        "status": "ACTIVE",
        "utilization": 88,
        "peak_hours": "17:00-22:00",
        "ai_efficiency": "Elite",
        "tags": ["AI RECOMMENDED"],
        "color": "#1a3a2a",
        "courts": [
            {"number": "01", "surface": "Premium Synthetic"},
            {"number": "02", "surface": "Standard Wood"},
            {"number": "03", "surface": "Premium Synthetic"},
            {"number": "04", "surface": "Premium Synthetic"},
        ],
    },
    {
        "id": "sky-02",
        "name": "Skyline Arena Football",
        "short_name": "Skyline Arena",
        "sport": "Football",
        "rating": 4.7,
        "reviews": 85,
        "location": "Thonglor District",
        "address": "42 Thonglor Soi 15",
        "district": "Thong Lor",
        "price_per_hour": 1200,
        "prime_price": 1800,
        "amenities": [
            {"icon": "ac_unit", "label": "Climate", "value": "Open Air"},
            {"icon": "local_parking", "label": "Parking", "value": "20 Slots"},
            {"icon": "checkroom", "label": "Facilities", "value": "Locker Rooms"},
            {"icon": "water_drop", "label": "Water", "value": "Dispenser"},
        ],
        "surface": "Artificial Turf",
        "status": "ACTIVE",
        "utilization": 76,
        "peak_hours": "18:00-21:00",
        "ai_efficiency": "High",
        "tags": ["LIVE AVAILABILITY"],
        "color": "#1a2a3a",
        "courts": [
            {"number": "01", "surface": "Artificial Turf"},
            {"number": "02", "surface": "Artificial Turf"},
        ],
    },
    {
        "id": "dwn-03",
        "name": "Downtown Hoops",
        "short_name": "Downtown Hoops",
        "sport": "Basketball",
        "rating": 4.5,
        "reviews": 62,
        "location": "Ari Soi 4",
        "address": "15 Ari Soi 4",
        "district": "Ari",
        "price_per_hour": 600,
        "prime_price": 900,
        "amenities": [
            {"icon": "ac_unit", "label": "Climate", "value": "Open Air"},
            {"icon": "local_parking", "label": "Parking", "value": "10 Slots"},
            {"icon": "checkroom", "label": "Facilities", "value": "Basic"},
            {"icon": "water_drop", "label": "Water", "value": "Vending"},
        ],
        "surface": "Hardwood",
        "status": "ACTIVE",
        "utilization": 65,
        "peak_hours": "17:00-20:00",
        "ai_efficiency": "Moderate",
        "tags": [],
        "color": "#2a1a1a",
        "courts": [
            {"number": "01", "surface": "Hardwood"},
            {"number": "02", "surface": "Outdoor Concrete"},
        ],
    },
    {
        "id": "pdl-04",
        "name": "Padel House Sukhumvit",
        "short_name": "Padel House",
        "sport": "Padel",
        "rating": 4.2,
        "reviews": 38,
        "location": "Sukhumvit Soi 39",
        "address": "42/1 Soi Sukhumvit 26",
        "district": "Sukhumvit",
        "price_per_hour": 800,
        "prime_price": 1100,
        "amenities": [
            {"icon": "ac_unit", "label": "Climate", "value": "Indoor AC"},
            {"icon": "local_parking", "label": "Parking", "value": "15 Slots"},
            {"icon": "checkroom", "label": "Facilities", "value": "Pro Shop"},
            {"icon": "water_drop", "label": "Water", "value": "Café"},
        ],
        "surface": "Professional Mat",
        "status": "ACTIVE",
        "utilization": 71,
        "peak_hours": "16:00-20:00",
        "ai_efficiency": "High",
        "tags": ["NEW"],
        "color": "#1a1a2a",
        "courts": [
            {"number": "01", "surface": "Professional Mat"},
            {"number": "02", "surface": "Professional Mat"},
        ],
    },
    {
        "id": "ryl-05",
        "name": "Royal Bangkok Sports Club",
        "short_name": "Royal Bangkok",
        "sport": "Badminton",
        "rating": 5.0,
        "reviews": 210,
        "location": "Pathumwan",
        "address": "1 Henri Dunant Rd",
        "district": "Sukhumvit",
        "price_per_hour": 950,
        "prime_price": 1400,
        "amenities": [
            {"icon": "ac_unit", "label": "Climate", "value": "Full AC"},
            {"icon": "local_parking", "label": "Parking", "value": "100+ Slots"},
            {"icon": "checkroom", "label": "Facilities", "value": "Full Service"},
            {"icon": "water_drop", "label": "Water", "value": "Spa & Café"},
        ],
        "surface": "Club Surface",
        "status": "ACTIVE",
        "utilization": 92,
        "peak_hours": "06:00-22:00",
        "ai_efficiency": "Elite",
        "tags": [],
        "color": "#0a2a1a",
        "courts": [
            {"number": "01", "surface": "Club Surface"},
            {"number": "02", "surface": "Club Surface"},
            {"number": "03", "surface": "Club Surface"},
        ],
    },
    {
        "id": "imp-06",
        "name": "Impact Volleyball Hall",
        "short_name": "Impact Volleyball",
        "sport": "Basketball",
        "rating": 4.8,
        "reviews": 95,
        "location": "Muang Thong Thani",
        "address": "99 Popular Rd",
        "district": "Thong Lor",
        "price_per_hour": 350,
        "prime_price": 550,
        "amenities": [
            {"icon": "ac_unit", "label": "Climate", "value": "Full AC"},
            {"icon": "local_parking", "label": "Parking", "value": "200+ Slots"},
            {"icon": "checkroom", "label": "Facilities", "value": "Multi-Purpose Hall"},
            {"icon": "water_drop", "label": "Water", "value": "Canteen"},
        ],
        "surface": "Indoor Acrylic",
        "status": "ACTIVE",
        "utilization": 80,
        "peak_hours": "17:00-21:00",
        "ai_efficiency": "High",
        "tags": ["AI POWERED PRICING"],
        "color": "#2a2a1a",
        "courts": [
            {"number": "01", "surface": "Indoor Acrylic"},
            {"number": "02", "surface": "Indoor Acrylic"},
            {"number": "03", "surface": "Indoor Acrylic"},
            {"number": "04", "surface": "Indoor Acrylic"},
        ],
    },
]


def get_time_slots(court_id="bbc-01"):
    """Generate time slots for a given court."""
    slots = []
    base_prices = {"bbc-01": 450, "sky-02": 1200, "dwn-03": 600, "pdl-04": 800, "ryl-05": 950, "imp-06": 350}
    base = base_prices.get(court_id, 450)
    for hour in range(8, 23):
        is_peak = 17 <= hour <= 21
        price = int(base * 1.4) if is_peak else base
        if hour in [11, 19]:
            status = "booked"
        elif hour == 14:
            status = "maintenance"
        else:
            status = "available"
        # AI pricing tag for select slots
        ai_tag = "AI PRECISION PRICING" if hour in [10, 18] else None
        slots.append({
            "time_start": f"{hour:02d}:00",
            "time_end": f"{hour+1:02d}:00",
            "price": price,
            "status": status,
            "ai_tag": ai_tag,
        })
    return slots


PLAYER_BOOKINGS = [
    {
        "id": "ZP-94821",
        "court_id": "bbc-01",
        "court_name": "Bangkok Badminton Center",
        "court_number": "04",
        "surface": "Premium Synthetic",
        "date": "Sat, 24 Oct",
        "date_full": "Saturday, October 24, 2026",
        "time_start": "18:00",
        "time_end": "20:00",
        "duration_min": 120,
        "status": "CONFIRMED",
        "base_price": 600,
        "discount": 80,
        "service_fee": 25,
        "total": 545,
        "payment_method": "Credit/Debit",
        "ai_verified": True,
        "team_members": ["Narin S.", "Krit B.", "Ball T."],
        "qr_code": "ZP-294-8X1",
        "address": "88 Ratchadapisek Rd.",
        "address_note": "15 min from your location",
        "color": "#1a3a2a",
    },
    {
        "id": "ZP-94835",
        "court_id": "pdl-04",
        "court_name": "Padel House Sukhumvit",
        "court_number": "01",
        "surface": "Professional Mat",
        "date": "Wed, 28 Oct",
        "date_full": "Wednesday, October 28, 2026",
        "time_start": "07:00",
        "time_end": "08:30",
        "duration_min": 90,
        "status": "CONFIRMED",
        "base_price": 800,
        "discount": 0,
        "service_fee": 25,
        "total": 825,
        "payment_method": "PromptPay",
        "ai_verified": False,
        "team_members": [],
        "qr_code": "ZP-312-4K2",
        "address": "42/1 Soi Sukhumvit 26, Khlong Tan, Khlong Toei, Bangkok 10110",
        "address_note": "",
        "color": "#1a1a2a",
    },
]


OWNER_VENUES = [
    {
        "id": "venue-01",
        "name": "Main Arena",
        "location": "BANGKOK CENTRAL",
        "courts_count": 6,
        "revenue_today": 1240,
        "color": "#1a3a2a",
    },
    {
        "id": "venue-02",
        "name": "Ari Sports Center",
        "location": "PHAYA THAI, BANGKOK",
        "courts_count": 4,
        "revenue_today": 890,
        "color": "#1a2a3a",
    },
    {
        "id": "venue-03",
        "name": "Sukhumvit Padel",
        "location": "KLONG TOEY, BANGKOK",
        "courts_count": 3,
        "revenue_today": 2150,
        "color": "#2a1a2a",
    },
]


OWNER_BOOKINGS = [
    {
        "customer": "Marcus Sterling",
        "member_id": "#ZP-2940",
        "court": "Center Court",
        "sport": "Padel",
        "time": "14:00 - 15:30 (90 min)",
        "status": "BOOKED",
        "avatar_color": "#506300",
    },
    {
        "customer": "Elena Rodriguez",
        "member_id": "#ZP-5811",
        "court": "Practice Wall 2",
        "sport": "Tennis",
        "time": "10:00 - 11:00 (60 min)",
        "status": "COMPLETED",
        "avatar_color": "#615e00",
    },
    {
        "customer": "Jonathan Wu",
        "member_id": "#ZP-1087",
        "court": "West Pitch",
        "sport": "Soccer",
        "time": "16:00 - 20:00 (240 min)",
        "status": "CANCELLED",
        "avatar_color": "#b02500",
    },
    {
        "customer": "Sarah Connor",
        "member_id": "#ZP-0622",
        "court": "High-Perf Studio",
        "sport": "Yoga",
        "time": "18:00 - 19:00 (60 min)",
        "status": "BOOKED",
        "avatar_color": "#3a506b",
    },
]


WEEKLY_UTILIZATION = {
    "Mon": 65,
    "Tue": 72,
    "Wed": 58,
    "Thu": 80,
    "Fri": 91,
    "Sat": 88,
    "Sun": 45,
}

DISTRICT_DEMAND = [
    {"name": "Sukhumvit", "demand": 94, "level": "Peak"},
    {"name": "Ari District", "demand": 62, "level": "Moderate"},
    {"name": "Thong Lor", "demand": 98, "level": "Saturated"},
]

TODAYS_BOOKINGS = [
    {"time": "17:00", "type": "PM", "title": "Padel Championship Practice", "customer": "Amanda S.", "venue": "Sukhumvit Padel", "status": "CONFIRMED"},
    {"time": "18:30", "type": "PM", "title": "Casual Tennis Session", "customer": "Michael W.", "venue": "Ari Sports Center", "status": "IN PROGRESS"},
    {"time": "20:00", "type": "PM", "title": "Late Night Badminton", "customer": "Sarah L.", "venue": "Ari Sports Center", "status": "UPCOMING"},
]

SLOT_CALENDAR = {
    0: [  # Monday
        {"time": "08:00-10:00", "label": "Advanced Padel", "type": "booking", "color": "#e2e7ff"},
        {"time": "14:00-15:00", "label": "Maintenance", "type": "maintenance", "color": "#ffddcc"},
    ],
    1: [  # Tuesday
        {"time": "10:00-12:00", "label": "Open Booking", "type": "open", "color": "#f0ffc0"},
    ],
    2: [  # Wednesday
        {"time": "09:00-11:00", "label": "Maintenance", "type": "maintenance", "color": "#ffddcc"},
        {"time": "16:00-18:00", "label": "Open Booking", "type": "open", "color": "#f0ffc0"},
        {"time": "19:00-21:00", "label": "Pickleball Slam", "type": "booking", "color": "#e2e7ff"},
    ],
    3: [],  # Thursday
    4: [],  # Friday
    5: [  # Saturday
        {"time": "08:00-12:00", "label": "Tournament", "type": "booking", "color": "#e2e7ff"},
    ],
    6: [],  # Sunday
}

FEEDBACK_TAGS = ["Clean Courts", "Good Lighting", "Great Staff", "Easy Access", "Pro Grade Gear"]

SPORTS_LIST = ["Badminton", "Football", "Basketball", "Padel"]
SPORTS_ICONS = {"Badminton": "🏸", "Football": "⚽", "Basketball": "🏀", "Padel": "🎾"}

DISTRICTS = ["All Districts", "Sukhumvit", "Thong Lor", "Ari", "Pathumwan", "Silom"]
