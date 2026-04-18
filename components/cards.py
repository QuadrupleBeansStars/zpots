"""Reusable card components for ZPOTS."""
import streamlit as st
from components.nav import navigate


def court_card(court, key_prefix="court", show_book=True):
    SPORT_ICON = {"Badminton":"🏸","Football":"⚽","Basketball":"🏀","Padel":"🎾","Tennis":"🎾"}
    tags_html = " ".join(
        f'<span class="ai-tag" style="margin-bottom:4px;">{t}</span>'
        for t in court.get("tags", [])
    )
    st.markdown(f"""
    <div class="zpots-card" style="padding:0; overflow:hidden;">
        <div style="height:150px; background:linear-gradient(135deg,{court['color']},{court['color']}cc);
                    border-radius:16px 16px 0 0; position:relative;
                    display:flex; align-items:center; justify-content:center;">
            <span style="font-size:2.75rem; color:rgba(255,255,255,0.9);">
                {SPORT_ICON.get(court['sport'], '🏸')}</span>
            <div style="position:absolute; top:12px; left:12px;">{tags_html}</div>
        </div>
        <div style="padding:14px 16px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="font-family:'Inter'; font-weight:600; font-size:14px; color:#1c2526;">
                    {court['name']}</span>
                <span style="font-size:13px; color:#506300;">⭐ {court['rating']}</span>
            </div>
            <div style="font-size:12px; color:#3d4455; margin-top:4px;">📍 {court['location']}</div>
            <div style="margin-top:12px;">
                <span class="eyebrow" style="font-size:9px;">STARTS AT</span><br/>
                <span class="display" style="font-size:20px;">฿{court['price_per_hour']}</span>
                <span style="font-size:11px; color:#3d4455;"> /hr</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if show_book:
        if st.button("Book Now", key=f"{key_prefix}_{court['id']}_book",
                     type="primary", width='stretch'):
            navigate("court_details", selected_court_id=court["id"])


def kpi_card(label, value, delta=None, icon=None):
    icon_html  = f'<span style="font-size:18px; display:block; margin-bottom:4px;">{icon}</span>' if icon else ""
    delta_html = f'<div style="font-size:12px; color:#2E6B00; margin-top:2px;">{delta}</div>' if delta else ""
    st.markdown(f"""
    <div class="kpi-card">
        {icon_html}
        <div class="eyebrow">{label}</div>
        <div class="display" style="font-size:28px;">{value}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)


def booking_card_player(booking, key_prefix="pbk"):
    SPORT_ICON = {"Badminton":"🏸","Football":"⚽","Basketball":"🏀","Padel":"🎾","Tennis":"🎾"}
    ai_badge = '<div style="position:absolute;top:8px;left:8px;"><span class="ai-tag">AI CONFIRMED</span></div>' \
               if booking.get("ai_verified") else ""
    status_cls = f"status-{booking['status'].lower()}"
    team_colors = ["#2E6B00","#1E4A00","#3a506b"]
    team_html = "".join(
        f'<span style="display:inline-block;width:28px;height:28px;border-radius:50%;'
        f'background:{team_colors[i%3]};color:white;text-align:center;line-height:28px;'
        f'font-size:11px;margin-right:-6px;border:2px solid white;">{m[0]}</span>'
        for i, m in enumerate(booking.get("team_members",[])[:3])
    )
    st.markdown(f"""
    <div class="zpots-card" style="display:flex; gap:20px; padding:20px; align-items:flex-start;">
        <div style="width:180px; min-width:180px; height:120px; border-radius:12px;
                    background:linear-gradient(135deg,{booking['color']},{booking['color']}cc);
                    display:flex; align-items:center; justify-content:center; position:relative;">
            <span style="font-size:2rem;">{SPORT_ICON.get(booking.get('sport','Badminton'),'🏸')}</span>
            {ai_badge}
        </div>
        <div style="flex:1;">
            <div style="font-weight:700; font-size:18px; color:#1c2526;">{booking['court_name']}</div>
            <div style="display:flex; gap:20px; margin-top:8px; font-size:13px; color:#3d4455;">
                <span>📅 {booking['date']}</span>
                <span>🕐 {booking['time_start']} – {booking['time_end']}</span>
            </div>
            <div style="margin-top:10px; display:flex; gap:6px; align-items:center;">
                <span class="status-badge {status_cls}">{booking['status']}</span>
                <span style="font-size:12px; color:#3d4455;">
                    Booking #{booking.get('id','ZP-00000')}</span>
            </div>
            <div style="margin-top:10px;">{team_html}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🎫 View QR", key=f"{key_prefix}_{booking['id']}_qr", type="primary"):
        navigate("checkin_qr", selected_booking_id=booking["id"])


def venue_card_owner(venue, key_prefix="ven"):
    st.markdown(f"""
    <div class="zpots-card" style="padding:0; overflow:hidden;">
        <div style="height:70px; background:linear-gradient(135deg,{venue['color']},{venue['color']}cc);
                    display:flex; align-items:center; justify-content:center;
                    border-radius:16px 16px 0 0;">
            <span style="font-size:24px; color:rgba(255,255,255,0.85);">🏟</span>
        </div>
        <div style="padding:12px 14px;">
            <div style="font-weight:600; font-size:14px; color:#1c2526;">{venue['name']}</div>
            <div class="eyebrow" style="font-size:9px; margin-top:2px;">{venue['location']}</div>
            <div style="display:flex; justify-content:space-between; margin-top:6px;
                        font-size:12px; color:#3d4455;">
                <span>{venue.get('courts_count',0)} courts</span>
                <span class="display" style="color:#2E6B00; font-size:14px;">
                    ฿{venue.get('revenue_today',0)}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Edit", key=f"{key_prefix}_{venue['id']}", width='stretch'):
        navigate("manage_courts")
