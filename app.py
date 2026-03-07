import streamlit as st
from datetime import datetime, timedelta

# Page config
st.set_page_config(
    page_title="Sports Field Booking Platform",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'manager_logged_in' not in st.session_state:
    st.session_state.manager_logged_in = False
if 'player_logged_in' not in st.session_state:
    st.session_state.player_logged_in = False
if 'manager_page' not in st.session_state:
    st.session_state.manager_page = 'Login'
if 'player_page' not in st.session_state:
    st.session_state.player_page = 'Splash'
if 'selected_match' not in st.session_state:
    st.session_state.selected_match = None
if 'booking_confirmed' not in st.session_state:
    st.session_state.booking_confirmed = False

# Dummy data - Bangkok themed
FIELDS_DATA = {
    'bangna': {
        'name': 'Bangna Football Arena',
        'description': 'Indoor futsal field with parking and showers',
        'address': 'Bangna-Trad Rd, Bangna, Bangkok',
        'location': 'Bangna',
        'type': '5v5 Football'
    },
    'rama9': {
        'name': 'Rama 9 Sports Center',
        'description': 'Outdoor football pitch with professional lighting',
        'address': 'Rama 9 Rd, Huai Khwang, Bangkok',
        'location': 'Rama 9',
        'type': '7v7 Football'
    },
    'ladprao': {
        'name': 'Ladprao Futsal Hub',
        'description': 'Modern indoor facility with air conditioning',
        'address': 'Ladprao Rd, Chatuchak, Bangkok',
        'location': 'Ladprao',
        'type': '5v5 Futsal'
    },
    'sukhumvit': {
        'name': 'Sukhumvit Arena',
        'description': 'Premium indoor sports complex',
        'address': 'Sukhumvit Rd, Khlong Toei, Bangkok',
        'location': 'Sukhumvit',
        'type': '6v6 Football'
    }
}

MATCHES_DATA = [
    {
        'id': 1,
        'field': 'bangna',
        'time': '19:00',
        'date': 'Today',
        'players_joined': ['Somchai', 'Narin', 'Krit', 'Ball', 'Tong', 'Num'],
        'max_players': 10,
        'price': 150,
        'type': '5v5 Football'
    },
    {
        'id': 2,
        'field': 'rama9',
        'time': '20:00',
        'date': 'Today',
        'players_joined': ['Arm', 'Poom', 'Joe', 'Mark'],
        'max_players': 10,
        'price': 120,
        'type': '7v7 Football'
    },
    {
        'id': 3,
        'field': 'ladprao',
        'time': '18:00',
        'date': 'Tomorrow',
        'players_joined': ['Bee', 'Top', 'Nick', 'James', 'Win'],
        'max_players': 10,
        'price': 180,
        'type': '5v5 Futsal'
    },
    {
        'id': 4,
        'field': 'sukhumvit',
        'time': '21:00',
        'date': 'Today',
        'players_joined': ['Golf', 'Bank'],
        'max_players': 12,
        'price': 200,
        'type': '6v6 Football'
    }
]

BOOKINGS_DATA = [
    {'time': '14:00', 'player': 'Team Somchai', 'status': 'Confirmed', 'field': 'Bangna Football Arena'},
    {'time': '15:00', 'player': 'Office Team', 'status': 'Confirmed', 'field': 'Rama 9 Sports Center'},
    {'time': '18:00', 'player': 'Open Match', 'status': 'Available', 'field': 'Bangna Football Arena'},
    {'time': '19:00', 'player': 'Open Match', 'status': 'Available', 'field': 'Ladprao Futsal Hub'},
    {'time': '20:00', 'player': 'Corporate Booking', 'status': 'Confirmed', 'field': 'Sukhumvit Arena'},
]

TIME_SLOTS = [
    {'time': '08:00', 'status': 'Available'},
    {'time': '09:00', 'status': 'Available'},
    {'time': '10:00', 'status': 'Blocked'},
    {'time': '11:00', 'status': 'Available'},
    {'time': '12:00', 'status': 'Available'},
    {'time': '13:00', 'status': 'Available'},
    {'time': '14:00', 'status': 'Booked'},
    {'time': '15:00', 'status': 'Booked'},
    {'time': '16:00', 'status': 'Available'},
    {'time': '17:00', 'status': 'Available'},
    {'time': '18:00', 'status': 'Available'},
    {'time': '19:00', 'status': 'Available'},
    {'time': '20:00', 'status': 'Available'},
]

# =====================================================
# B2B MANAGER PORTAL
# =====================================================

def manager_portal():
    st.title("⚽ Field Manager Portal")

    if not st.session_state.manager_logged_in:
        show_manager_login()
    else:
        # Navigation
        with st.sidebar:
            st.subheader("📋 Manager Menu")

            menu_options = ["Dashboard", "Fields", "Schedule", "Pricing", "Bookings"]
            selected = st.radio(
                "Navigate to:",
                menu_options,
                index=menu_options.index(st.session_state.manager_page) if st.session_state.manager_page in menu_options else 0,
                label_visibility="collapsed"
            )

            if selected != st.session_state.manager_page:
                st.session_state.manager_page = selected
                st.rerun()

            st.divider()

            if st.button("Logout", use_container_width=True):
                st.session_state.manager_logged_in = False
                st.session_state.manager_page = 'Login'
                st.rerun()

        # Show selected page
        if st.session_state.manager_page == "Dashboard":
            show_manager_dashboard()
        elif st.session_state.manager_page == "Fields":
            show_field_management()
        elif st.session_state.manager_page == "Schedule":
            show_schedule_management()
        elif st.session_state.manager_page == "Pricing":
            show_pricing_management()
        elif st.session_state.manager_page == "Bookings":
            show_bookings_view()

def show_manager_login():
    st.markdown("### Login to Dashboard")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.text_input("Email", placeholder="manager@example.com")
        st.text_input("Password", type="password", placeholder="Enter password")

        if st.button("Login to Dashboard", use_container_width=True, type="primary"):
            st.session_state.manager_logged_in = True
            st.session_state.manager_page = 'Dashboard'
            st.rerun()

        st.caption("Forgot password?")

def show_manager_dashboard():
    st.header("Dashboard")

    # Today's summary
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Bookings Today", "12")

    with col2:
        st.metric("Revenue Today", "฿7,800")

    with col3:
        st.metric("Available Slots", "8")

    st.divider()

    # Upcoming bookings
    st.subheader("Upcoming Bookings")

    upcoming = [
        {'time': '18:00', 'match': 'Team A vs Team B'},
        {'time': '19:00', 'match': 'Casual Match'},
        {'time': '20:00', 'match': 'Corporate Booking'},
    ]

    for booking in upcoming:
        st.info(f"**{booking['time']}** - {booking['match']}")

def show_field_management():
    st.header("Field Management")

    st.subheader("Add New Field")

    col1, col2 = st.columns(2)

    with col1:
        field_name = st.text_input("Field Name", value="Bangna Football Arena")
        description = st.text_area("Description", value="Indoor futsal field with parking and showers")
        address = st.text_input("Address", value="Bangna-Trad Rd, Bangna, Bangkok")

    with col2:
        st.write("Upload Images")
        st.file_uploader("Image 1", type=['png', 'jpg', 'jpeg'])
        st.file_uploader("Image 2", type=['png', 'jpg', 'jpeg'])
        st.file_uploader("Image 3", type=['png', 'jpg', 'jpeg'])

    st.write("Location")
    st.map(data={'lat': [13.6644], 'lon': [100.6125]}, zoom=12)

    if st.button("Save Field", type="primary"):
        st.success("✅ Field saved successfully!")

def show_schedule_management():
    st.header("Schedule Management")

    st.subheader("Bangna Football Arena")
    st.caption("Date: 12 July 2026")

    st.divider()

    # Time slots grid
    for slot in TIME_SLOTS:
        col1, col2, col3 = st.columns([1, 2, 1])

        with col1:
            st.write(f"**{slot['time']}**")

        with col2:
            if slot['status'] == 'Available':
                st.success(f"✅ {slot['status']}")
            elif slot['status'] == 'Booked':
                st.error(f"📅 {slot['status']}")
            else:
                st.warning(f"🚫 Maintenance (Blocked)")

        with col3:
            if slot['status'] == 'Available':
                if st.button("Block", key=f"block_{slot['time']}"):
                    st.info("Slot blocked")
            elif slot['status'] == 'Blocked':
                if st.button("Enable", key=f"enable_{slot['time']}"):
                    st.info("Slot enabled")

def show_pricing_management():
    st.header("Pricing Settings")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Off-Peak Price")
        st.caption("08:00 - 16:00")
        off_peak = st.number_input("Price per hour (฿)", value=1000, step=100, key="off_peak")

        st.divider()

        st.subheader("Peak Price")
        st.caption("17:00 - 22:00")
        peak = st.number_input("Price per hour (฿)", value=1500, step=100, key="peak")

    with col2:
        st.subheader("Weekend Price")
        st.caption("All day Saturday & Sunday")
        weekend = st.number_input("Price per hour (฿)", value=1800, step=100, key="weekend")

    st.divider()

    if st.button("Save Pricing", type="primary"):
        st.success("✅ Pricing updated successfully!")

def show_bookings_view():
    st.header("Bookings - Today")

    st.divider()

    # Create a table
    import pandas as pd
    df = pd.DataFrame(BOOKINGS_DATA)

    # Style the dataframe
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "time": "Time",
            "player": "Player Name",
            "status": st.column_config.TextColumn(
                "Status",
            ),
            "field": "Field"
        }
    )

# =====================================================
# B2C PLAYER APP
# =====================================================

def player_app():
    st.title("⚽ PLAYMATCH BANGKOK")

    # Custom CSS for mobile-like experience
    st.markdown("""
        <style>
        .match-card {
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 15px;
        }
        .match-title {
            font-size: 20px;
            font-weight: bold;
            color: #1f1f1f;
        }
        .match-detail {
            font-size: 14px;
            color: #555;
        }
        .player-badge {
            background-color: #4CAF50;
            color: white;
            padding: 5px 10px;
            border-radius: 5px;
            display: inline-block;
            margin: 5px;
        }
        </style>
    """, unsafe_allow_html=True)

    if not st.session_state.player_logged_in:
        show_player_splash()
    else:
        # Show different pages based on navigation
        if st.session_state.booking_confirmed:
            show_booking_confirmation()
        elif st.session_state.selected_match:
            show_match_detail()
        else:
            show_player_home()

def show_player_splash():
    st.markdown("### Find football games near you")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.write("")
        st.write("")

        if st.button("Login", use_container_width=True, type="primary"):
            st.session_state.player_logged_in = True
            st.rerun()

        if st.button("Create Account", use_container_width=True):
            st.session_state.player_logged_in = True
            st.rerun()

def show_player_home():
    st.subheader("📍 Bangkok")
    st.caption("Nearby Matches")

    st.divider()

    for match in MATCHES_DATA:
        field = FIELDS_DATA[match['field']]

        with st.container():
            col1, col2 = st.columns([3, 1])

            with col1:
                st.markdown(f"### ⚽ {field['name']}")
                st.write(f"**{match['date']} {match['time']}**")
                st.write(f"{match['type']}")
                st.write(f"Players Joined: **{len(match['players_joined'])} / {match['max_players']}**")
                st.write(f"Price: **฿{match['price']}**")

            with col2:
                st.write("")
                st.write("")
                if st.button("View Match", key=f"view_{match['id']}", use_container_width=True):
                    st.session_state.selected_match = match['id']
                    st.rerun()

        st.divider()

    # Back button
    if st.button("← Logout", use_container_width=True):
        st.session_state.player_logged_in = False
        st.session_state.selected_match = None
        st.session_state.booking_confirmed = False
        st.rerun()

def show_match_detail():
    match = next(m for m in MATCHES_DATA if m['id'] == st.session_state.selected_match)
    field = FIELDS_DATA[match['field']]

    st.header(field['name'])

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**Time:** {match['time']} - {int(match['time'].split(':')[0]) + 1}:00")
        st.write(f"**Format:** {match['type']}")
        st.write(f"**Price:** ฿{match['price']}")

    with col2:
        remaining = match['max_players'] - len(match['players_joined'])
        st.write(f"**Remaining Slots:** {remaining}")

    st.divider()

    st.subheader("Players Joined")

    # Show players as badges
    cols = st.columns(4)
    for idx, player in enumerate(match['players_joined']):
        with cols[idx % 4]:
            st.markdown(f'<div class="player-badge">{player}</div>', unsafe_allow_html=True)

    st.write("")
    st.write("")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("← Back to Matches", use_container_width=True):
            st.session_state.selected_match = None
            st.rerun()

    with col2:
        if st.button("Join Match", use_container_width=True, type="primary"):
            st.session_state.booking_confirmed = True
            st.rerun()

def show_booking_confirmation():
    match = next(m for m in MATCHES_DATA if m['id'] == st.session_state.selected_match)
    field = FIELDS_DATA[match['field']]

    st.success("🎉 Booking Confirmed")

    st.divider()

    st.write(f"**Match:** {field['name']}")
    st.write(f"**Time:** {match['time']}")
    st.write(f"**Price:** ฿{match['price']}")

    st.divider()

    st.subheader("Address")
    st.write(field['address'])

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Open Map", use_container_width=True):
            st.info("Opening map...")

    with col2:
        if st.button("View Booking", use_container_width=True):
            st.info("Viewing booking details...")

    st.write("")

    if st.button("← Back to Home", use_container_width=True):
        st.session_state.selected_match = None
        st.session_state.booking_confirmed = False
        st.rerun()

# =====================================================
# MAIN APP
# =====================================================

def main():
    # Top-level tabs
    tab1, tab2 = st.tabs(["🏢 Field Manager Portal (B2B)", "📱 Player App (B2C)"])

    with tab1:
        manager_portal()

    with tab2:
        player_app()

if __name__ == "__main__":
    main()
