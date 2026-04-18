"""Court Search Results - Find Your Court."""
import streamlit as st
from components.css import inject_global_css
from components.nav import navigate, render_player_topbar
from components.cards import court_card
from data.dummy_data import COURTS, SPORTS_LIST, DISTRICTS
from utils.gemini import parse_search_query


def render():
    inject_global_css()
    render_player_topbar()

    st.markdown("""
    <div style="margin-bottom:1.5rem;">
        <div class="eyebrow" style="font-size:11px;">BANGKOK PRECISION SEARCH</div>
        <h1 style="font-family:'Space Grotesk';font-size:2rem;font-weight:700;
                   letter-spacing:-0.01em;color:#1c2526;margin-top:4px;">Find Your Court</h1>
    </div>
    """, unsafe_allow_html=True)

    # --- Natural Language Search ---
    nl_col, btn_col = st.columns([5, 1])
    with nl_col:
        nl_query = st.text_input(
            "AI Search",
            placeholder='e.g. "badminton near Sukhumvit Friday evening under 400 baht"',
            label_visibility="collapsed",
            key="nl_search_input",
        )
    with btn_col:
        nl_submit = st.button("Search", type="primary", width='stretch', key="nl_search_btn")

    # Run Gemini when button pressed or query changes
    if nl_submit and nl_query.strip():
        with st.spinner("AI is parsing your search..."):
            filters = parse_search_query(nl_query.strip())
        st.session_state.nl_filters = filters
        st.session_state.nl_query_used = nl_query.strip()
        st.rerun()
    elif not nl_query.strip() and st.session_state.get("nl_filters") is not None:
        st.session_state.nl_filters = None
        st.session_state.nl_query_used = None
        st.rerun()

    # Show parsed filter chips
    nl_filters = st.session_state.get("nl_filters")
    if nl_filters:
        chips = []
        if nl_filters.get("sport"):
            chips.append(f"Sport: {nl_filters['sport']}")
        if nl_filters.get("district"):
            chips.append(f"District: {nl_filters['district']}")
        if nl_filters.get("time_of_day"):
            chips.append(f"Time: {nl_filters['time_of_day'].capitalize()}")
        if nl_filters.get("max_price"):
            chips.append(f"Max: ฿{nl_filters['max_price']}")

        if chips:
            chips_html = " &nbsp;·&nbsp; ".join(
                f'<span class="chip chip-selected" style="font-size:10px;padding:3px 10px;">{c}</span>'
                for c in chips
            )
            st.markdown(
                f'<div style="margin:6px 0 10px 0;">AI parsed &nbsp; {chips_html}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div style="margin:6px 0 10px 0; font-size:12px; color:#3d4455;">No specific filters detected — showing all courts.</div>',
                unsafe_allow_html=True,
            )

    # Inline sport chips (JSX SearchScreen pattern)
    sports_inline = ['All', 'Badminton', 'Football', 'Basketball', 'Padel']
    if "selected_sport" not in st.session_state:
        st.session_state.selected_sport = "All"

    chip_html = '<div style="display:flex;gap:8px;margin:12px 0 16px;align-items:center;">'
    chip_html += '<span class="eyebrow">SPORT</span>'
    for s in sports_inline:
        cls = "chip-selected" if st.session_state.get("selected_sport") == s else "chip-default"
        chip_html += f'<span class="chip {cls}">{s}</span>'
    chip_html += '</div>'
    st.markdown(chip_html, unsafe_allow_html=True)

    sport_btn_cols = st.columns(len(sports_inline) + 2)
    for i, s in enumerate(sports_inline):
        with sport_btn_cols[i]:
            if st.button(s, key=f"sport_chip_{s}",
                         type="primary" if st.session_state.get("selected_sport") == s else "secondary"):
                st.session_state.selected_sport = s
                st.rerun()

    # Filters in sidebar
    with st.sidebar:
        st.markdown("<h3 style='font-size:1rem;'>Sports</h3>", unsafe_allow_html=True)
        selected_sports = []
        sport_cols = st.columns(2)
        for i, sport in enumerate(SPORTS_LIST):
            with sport_cols[i % 2]:
                if st.checkbox(sport, value=False, key=f"sport_{sport}"):
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

    # --- Filtering logic ---
    filtered = list(COURTS)

    # Apply inline sport chip filter (when no NL filters active)
    selected_sport = st.session_state.get("selected_sport", "All")
    if not nl_filters and selected_sport != "All":
        filtered = [c for c in filtered if c["sport"] == selected_sport] or list(COURTS)

    # Apply NL filters (take precedence over sidebar when active)
    if nl_filters:
        if nl_filters.get("sport"):
            filtered = [c for c in filtered if c["sport"].lower() == nl_filters["sport"].lower()]
        if nl_filters.get("district"):
            filtered = [c for c in filtered if nl_filters["district"].lower() in c.get("district", "").lower()]
        if nl_filters.get("max_price"):
            filtered = [c for c in filtered if c["price_per_hour"] <= nl_filters["max_price"]]
        if nl_filters.get("time_of_day"):
            tod = nl_filters["time_of_day"].lower()
            tod_ranges = {"morning": range(6, 12), "afternoon": range(12, 17), "evening": range(17, 22)}
            hours = tod_ranges.get(tod, range(0, 24))

            def overlaps_peak(court):
                peak = court.get("peak_hours", "")
                try:
                    start_h = int(peak.split("-")[0].split(":")[0])
                    return start_h in hours
                except Exception:
                    return True

            filtered = [c for c in filtered if overlaps_peak(c)]
    else:
        # Sidebar sport filter
        if selected_sports:
            filtered = [c for c in filtered if c["sport"] in selected_sports] or list(COURTS)

    # Fallback: show all if nothing matched
    if not filtered:
        filtered = list(COURTS)

    # Top bar with view toggle and sort
    top1, top2, top3 = st.columns([2, 1, 1])
    with top1:
        st.markdown(f'<span class="eyebrow">SHOWING {len(filtered)} COURTS IN BANGKOK</span>',
                    unsafe_allow_html=True)
    with top2:
        view = st.radio("View", ["Grid", "Map View"], horizontal=True, key="view_toggle", label_visibility="collapsed")
    with top3:
        st.selectbox("Sort by", ["Highest Rated", "Lowest Price", "Closest"], key="sort_by", label_visibility="collapsed")

    # Court grid
    rows = [filtered[i:i+3] for i in range(0, len(filtered), 3)]
    for row_idx, row in enumerate(rows):
        cols = st.columns(3)
        for col_idx, court in enumerate(row):
            with cols[col_idx]:
                court_card(court, key_prefix=f"search_{row_idx}_{col_idx}")

    st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)
    col_center = st.columns([1, 1, 1])
    with col_center[1]:
        st.button("Load More Courts", width='stretch', key="load_more")
