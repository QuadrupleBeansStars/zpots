"""Court Search Results - Find Your Court."""
import streamlit as st
from components.css import inject_global_css
from components.nav import navigate, render_player_topbar
from components.cards import court_card
from data.dummy_data import COURTS, SPORTS_LIST, DISTRICTS


def render():
    inject_global_css()
    render_player_topbar()

    st.markdown("""
    <h1 style="font-size:2rem; margin-bottom:0;">Find Your Court</h1>
    <p style="font-family:'Lexend'; font-size:11px; text-transform:uppercase; letter-spacing:0.1em; color:#535b71;">Bangkok Precision Search</p>
    """, unsafe_allow_html=True)

    # Filters in sidebar
    with st.sidebar:
        st.markdown("<h3 style='font-size:1rem;'>Sports</h3>", unsafe_allow_html=True)
        selected_sports = []
        sport_cols = st.columns(2)
        for i, sport in enumerate(SPORTS_LIST):
            with sport_cols[i % 2]:
                if st.checkbox(sport, value=(sport == "Badminton"), key=f"sport_{sport}"):
                    selected_sports.append(sport)

        st.markdown("<h3 style='font-size:1rem; margin-top:1rem;'>Date</h3>", unsafe_allow_html=True)
        st.date_input("Select date", key="search_date", label_visibility="collapsed")

        st.markdown("<h3 style='font-size:1rem; margin-top:1rem;'>District</h3>", unsafe_allow_html=True)
        st.selectbox("District", DISTRICTS, key="search_district", label_visibility="collapsed")

        st.markdown("<h3 style='font-size:1rem; margin-top:1rem;'>Price / Hour</h3>", unsafe_allow_html=True)
        price_range = st.slider("Price range", 300, 2000, (300, 800), step=50, key="price_range", label_visibility="collapsed", format="฿%d")

        st.markdown("<h3 style='font-size:1rem; margin-top:1rem;'>Time of Day</h3>", unsafe_allow_html=True)
        st.checkbox("Morning (06:00-12:00)", value=True, key="time_morning")
        st.checkbox("Afternoon (12:00-17:00)", value=True, key="time_afternoon")
        st.checkbox("Evening (17:00-22:00)", value=True, key="time_evening")

    # Top bar with view toggle and sort
    top1, top2, top3 = st.columns([2, 1, 1])
    with top1:
        st.markdown(f"""
        <span style="font-family:'Lexend'; font-size:11px; text-transform:uppercase; letter-spacing:0.1em; color:#535b71;">
            SHOWING {len(COURTS)} COURTS IN BANGKOK
        </span>
        """, unsafe_allow_html=True)
    with top2:
        view = st.radio("View", ["Grid", "Map View"], horizontal=True, key="view_toggle", label_visibility="collapsed")
    with top3:
        st.selectbox("Sort by", ["Highest Rated", "Lowest Price", "Closest"], key="sort_by", label_visibility="collapsed")

    # Court grid
    filtered = COURTS
    if selected_sports:
        filtered = [c for c in COURTS if c["sport"] in selected_sports] or COURTS

    rows = [filtered[i:i+3] for i in range(0, len(filtered), 3)]
    for row_idx, row in enumerate(rows):
        cols = st.columns(3)
        for col_idx, court in enumerate(row):
            with cols[col_idx]:
                court_card(court, key_prefix=f"search_{row_idx}_{col_idx}")

    st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)
    col_center = st.columns([1, 1, 1])
    with col_center[1]:
        st.button("Load More Courts", use_container_width=True, key="load_more")
