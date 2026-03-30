"""Reusable card components for ZPOTS."""
import streamlit as st
from components.nav import navigate


def court_card(court, key_prefix="court", show_book=True):
    """Render a court card with image placeholder, info, and optional book button."""
    tags_html = ""
    for tag in court.get("tags", []):
        tags_html += f'<span class="ai-tag" style="margin-bottom:4px;">{tag}</span> '

    st.markdown(f"""
    <div class="zpots-card" style="padding:0; overflow:hidden; height:100%;">
        <div class="court-image" style="background: linear-gradient(135deg, {court['color']}, {court['color']}cc); height: 160px;">
            <span style="font-size:2.5rem;">{'🏸' if court['sport'] == 'Badminton' else '⚽' if court['sport'] == 'Football' else '🏀' if court['sport'] == 'Basketball' else '🎾'}</span>
            <div style="position:absolute; top:12px; left:12px;">{tags_html}</div>
        </div>
        <div style="padding: 1rem;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="font-family:'Inter'; font-weight:600; font-size:14px; color:#272e42;">{court['name']}</span>
                <span style="font-family:'Inter'; font-size:13px; color:#506300;">⭐ {court['rating']}</span>
            </div>
            <div style="font-family:'Inter'; font-size:12px; color:#535b71; margin-top:4px;">📍 {court['location']}</div>
            <div style="display:flex; justify-content:space-between; align-items:center; margin-top:12px;">
                <div>
                    <span style="font-family:'Lexend'; font-size:9px; text-transform:uppercase; letter-spacing:0.1em; color:#535b71;">STARTS AT</span><br>
                    <span style="font-family:'Space Grotesk'; font-weight:700; font-size:18px; color:#272e42;">฿{court['price_per_hour']}</span>
                    <span style="font-family:'Inter'; font-size:11px; color:#535b71;">/hr</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if show_book:
        if st.button("Book Now", key=f"{key_prefix}_{court['id']}_book", type="primary", use_container_width=True):
            navigate("court_details", selected_court_id=court["id"])


def kpi_card(label, value, delta=None, icon=None):
    """Render a KPI metric card."""
    delta_html = ""
    if delta:
        delta_html = f'<div class="kpi-delta">{delta}</div>'
    icon_html = ""
    if icon:
        icon_html = f'<span style="font-size:18px; margin-bottom:4px; display:block;">{icon}</span>'

    st.markdown(f"""
    <div class="kpi-card">
        {icon_html}
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)


def booking_card_player(booking, key_prefix="pbk"):
    """Render a player booking card."""
    status_class = f"status-{booking['status'].lower()}"
    ai_badge = '<span class="ai-tag">AI CONFIRMED</span>' if booking.get("ai_verified") else ""

    team_html = ""
    for i, member in enumerate(booking.get("team_members", [])[:3]):
        colors = ["#506300", "#615e00", "#3a506b"]
        team_html += f'<span style="display:inline-block; width:28px; height:28px; border-radius:50%; background:{colors[i % 3]}; color:white; text-align:center; line-height:28px; font-size:11px; margin-right:-6px; border: 2px solid white;">{member[0]}</span>'

    st.markdown(f"""
    <div class="zpots-card" style="display:flex; gap:1.5rem; align-items:flex-start;">
        <div class="court-image" style="background: linear-gradient(135deg, {booking['color']}, {booking['color']}cc); width:200px; min-width:200px; height:140px; border-radius:12px; position:relative;">
            <span style="font-size:2rem;">🏸</span>
            {ai_badge if booking.get('ai_verified') else ''}
        </div>
        <div style="flex:1;">
            <div style="font-family:'Inter'; font-weight:700; font-size:18px; color:#272e42;">{booking['court_name']}</div>
            <div style="display:flex; gap:1.5rem; margin-top:8px;">
                <span style="font-family:'Inter'; font-size:13px; color:#535b71;">📅 {booking['date']}</span>
                <span style="font-family:'Inter'; font-size:13px; color:#535b71;">🕐 {booking['time_start']} - {booking['time_end']}</span>
            </div>
            <div style="display:flex; justify-content:space-between; align-items:center; margin-top:16px;">
                <div>{team_html}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🎫 View QR", key=f"{key_prefix}_{booking['id']}_qr", type="primary"):
        navigate("checkin_qr", selected_booking_id=booking["id"])


def venue_card_owner(venue, key_prefix="ven"):
    """Render an owner venue card."""
    st.markdown(f"""
    <div class="zpots-card" style="padding:0; overflow:hidden;">
        <div class="court-image" style="background: linear-gradient(135deg, {venue['color']}, {venue['color']}cc); height:100px;">
            <span style="font-size:1.5rem;">🏟</span>
        </div>
        <div style="padding:1rem;">
            <div style="font-family:'Inter'; font-weight:600; font-size:14px;">{venue['name']}</div>
            <div style="font-family:'Lexend'; font-size:9px; text-transform:uppercase; letter-spacing:0.1em; color:#535b71; margin-top:2px;">{venue['location']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Edit", key=f"{key_prefix}_{venue['id']}", use_container_width=True):
        navigate("manage_courts")
