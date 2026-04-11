"""Court Details & Slot Selection."""
import streamlit as st
from components.css import inject_global_css
from components.nav import navigate, render_player_topbar
from data.dummy_data import COURTS, get_time_slots


def render():
    inject_global_css()
    render_player_topbar()

    court_id = st.session_state.get("selected_court_id", "bbc-01")
    court = next((c for c in COURTS if c["id"] == court_id), COURTS[0])
    slots = get_time_slots(court_id)

    # Initialize session state for selections
    if "selected_date_idx" not in st.session_state:
        st.session_state.selected_date_idx = 0
    if "selected_slot_idx" not in st.session_state:
        st.session_state.selected_slot_idx = None

    # Court images
    st.markdown(f"""
    <div style="display:grid; grid-template-columns:2fr 1fr 1fr; gap:8px; margin-bottom:1.5rem;">
        <div class="court-image" style="background:linear-gradient(135deg, {court['color']}, {court['color']}cc); height:250px; grid-row:span 2;">
            <span style="font-size:3rem;">🏸</span>
        </div>
        <div class="court-image" style="background:linear-gradient(135deg, {court['color']}aa, {court['color']}88); height:121px;">
            <span style="font-size:1.5rem;">🏸</span>
        </div>
        <div class="court-image" style="background:linear-gradient(135deg, {court['color']}88, {court['color']}66); height:121px;">
            <span style="font-size:1.5rem;">🏸</span>
        </div>
        <div class="court-image" style="background:linear-gradient(135deg, {court['color']}66, {court['color']}44); height:121px; position:relative;">
            <span style="font-size:1.5rem;">📸</span>
            <div style="position:absolute; bottom:8px; right:8px; background:rgba(0,0,0,0.6); color:white; padding:4px 10px; border-radius:8px; font-size:11px;">VIEW ALL PHOTOS</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Court info
    tags_html = " ".join(f'<span class="ai-tag">{t}</span>' for t in court.get("tags", []))
    st.markdown(f"""
    <div style="margin-bottom:0.5rem;">{tags_html}</div>
    <div style="display:flex; align-items:center; gap:8px; margin-bottom:4px;">
        <span style="font-family:'Inter'; font-size:13px; color:#506300;">⭐ {court['rating']} ({court['reviews']} reviews)</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"# {court['name'].upper()}")
    st.markdown(f"📍 {court['location']}")

    # Amenities
    st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)
    am_cols = st.columns(4)
    for i, amenity in enumerate(court["amenities"]):
        with am_cols[i]:
            st.markdown(f"""
            <div class="zpots-card-surface" style="text-align:center; padding:1rem;">
                <span style="font-size:1.3rem;">{'❄️' if i==0 else '🅿️' if i==1 else '🚿' if i==2 else '💧'}</span>
                <div style="font-family:'Lexend'; font-size:9px; text-transform:uppercase; letter-spacing:0.1em; color:#3d4455; margin-top:6px;">{amenity['label']}</div>
                <div style="font-family:'Inter'; font-weight:600; font-size:13px; color:#272e42;">{amenity['value']}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:1.5rem;'></div>", unsafe_allow_html=True)

    # Main content: slots + booking summary
    main_col, summary_col = st.columns([2, 1])

    with main_col:
        st.markdown("""
        <div class="zpots-card-surface" style="padding:1.5rem;">
            <h3 style="font-size:1.1rem; margin-bottom:1rem;">SELECT YOUR SLOT</h3>
        </div>
        """, unsafe_allow_html=True)

        # Date selector
        dates = [("MON", "12"), ("TUE", "13"), ("WED", "14"), ("THU", "15"), ("FRI", "16"), ("SAT", "17"), ("SUN", "18")]
        date_cols = st.columns(7)
        for i, (day, num) in enumerate(dates):
            with date_cols[i]:
                btn_type = "primary" if st.session_state.selected_date_idx == i else "secondary"
                if st.button(f"{day}\n{num}", key=f"date_{i}", width='stretch', type=btn_type):
                    st.session_state.selected_date_idx = i
                    st.rerun()

        # Time slots grid
        st.space("small")
        slot_rows = [slots[i:i+4] for i in range(0, len(slots), 4)]
        for row_idx, row in enumerate(slot_rows):
            slot_cols = st.columns(4, gap="small")
            for col_idx, slot in enumerate(row):
                flat_idx = row_idx * 4 + col_idx
                with slot_cols[col_idx]:
                    is_selected = st.session_state.selected_slot_idx == flat_idx
                    status = slot["status"]
                    is_available = status == "available"

                    # Status line
                    if status == "booked":
                        status_html = '<div style="font-size:10px; font-weight:600; color:#c62828;">Booked</div>'
                    elif status == "maintenance":
                        status_html = '<div style="font-size:10px; font-weight:600; color:#e65100;">Maintenance</div>'
                    else:
                        status_html = '<div style="font-size:10px; font-weight:600; color:#2e6b00;">Available</div>'

                    price_str = f"{slot['price']} THB" if is_available or status == "booked" else "—"
                    border = "box-shadow:0 0 0 2px #cffc00;" if is_selected else ""
                    opacity = "1" if is_available else "0.45"

                    st.markdown(f"""
                    <div class="zpots-card" style="
                        padding:0.75rem 0.4rem;
                        text-align:center;
                        opacity:{opacity};
                        height:88px;
                        display:flex;
                        flex-direction:column;
                        align-items:center;
                        justify-content:center;
                        gap:4px;
                        {border}
                    ">
                        <div style="font-size:11px; color:#3d5040; font-weight:500; white-space:nowrap;">{slot['time_start']} – {slot['time_end']}</div>
                        <div style="font-family:'Space Grotesk'; font-weight:700; font-size:15px; color:#1c2526;">{price_str}</div>
                        {status_html}
                    </div>
                    """, unsafe_allow_html=True)

                    # Always render a button so every cell has identical structure
                    if is_available:
                        if st.button("Select", key=f"slot_{flat_idx}", use_container_width=True):
                            st.session_state.selected_slot_idx = flat_idx
                            st.rerun()
                    else:
                        st.button("—", key=f"slot_{flat_idx}", use_container_width=True, disabled=True)

    with summary_col:
        selected_slot = slots[st.session_state.selected_slot_idx] if st.session_state.selected_slot_idx is not None else None
        date_info = dates[st.session_state.selected_date_idx]

        total_price = selected_slot["price"] * 2 if selected_slot else 900

        st.markdown(f"""
        <div class="zpots-card" style="position:sticky; top:1rem;">
            <div class="court-image" style="background:linear-gradient(135deg, {court['color']}, {court['color']}cc); height:120px; margin-bottom:1rem; border-radius:12px;">
                <span style="font-size:2rem;">📍</span>
            </div>
            <div style="font-family:'Inter'; font-size:11px; color:#3d4455;">GET DIRECTIONS ↗</div>
            <hr style="margin:1rem 0;">
            <h3 style="font-size:1rem; margin-bottom:1rem;">BOOKING SUMMARY</h3>
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:8px;">
                <span>📅</span>
                <span style="font-family:'Inter'; font-size:14px;">Monday, {date_info[1]}th Nov</span>
            </div>
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:12px;">
                <span>🕐</span>
                <span style="font-family:'Inter'; font-size:14px;">{selected_slot['time_start'] + ' - ' + selected_slot['time_end'] + ' (2 hrs)' if selected_slot else '-- : -- (select a slot)'}</span>
            </div>
            <hr>
            <div style="display:flex; justify-content:space-between; align-items:center; margin-top:12px;">
                <span style="font-family:'Lexend'; font-size:10px; text-transform:uppercase; letter-spacing:0.1em; color:#3d4455;">TOTAL PRICE</span>
            </div>
            <div style="font-family:'Space Grotesk'; font-weight:700; font-size:2rem; color:#272e42;">{total_price} THB</div>
            <div style="font-size:11px; color:#3d4455;">INCL. TAXES</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)
        if st.button("PROCEED TO BOOKING →", type="primary", width='stretch', key="proceed_booking"):
            if selected_slot is None:
                st.toast("Please select a time slot first.", icon="⚠️")
            else:
                st.session_state.booking_court = court
                st.session_state.booking_slot = selected_slot
                st.session_state.booking_total = total_price
                navigate("player_booking")

        st.markdown("""
        <div style="text-align:center; font-size:11px; color:#3d4455; margin-top:8px;">Free cancellation up to 1hr before</div>
        """, unsafe_allow_html=True)
