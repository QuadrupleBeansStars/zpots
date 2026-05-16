"""Reusable card components for ZPOTS."""
import streamlit as st
from components.nav import navigate


def court_card(court, key_prefix="court", show_book=True):
    SPORT_ICON = {"Badminton":"🏸","Football":"⚽","Basketball":"🏀","Padel":"🎾","Tennis":"🎾"}
    tags_html = " ".join(
        f'<span class="ai-tag" style="margin-bottom:4px;">{t}</span>'
        for t in court.get("tags", [])
    )
    html = (
        f'<div class="zpots-card" style="padding:0; overflow:hidden;">'
        f'<div style="height:150px; background:linear-gradient(135deg,{court["color"]},{court["color"]}cc);'
        f'border-radius:16px 16px 0 0; position:relative;'
        f'display:flex; align-items:center; justify-content:center;">'
        f'<span style="font-size:2.75rem; color:rgba(255,255,255,0.9);">{SPORT_ICON.get(court["sport"], "🏸")}</span>'
        f'<div style="position:absolute; top:12px; left:12px;">{tags_html}</div>'
        f'</div>'
        f'<div style="padding:14px 16px;">'
        f'<div style="display:flex; justify-content:space-between; align-items:center;">'
        f'<span style="font-family:\'Inter\'; font-weight:600; font-size:14px; color:#1c2526;">{court["name"]}</span>'
        f'<span style="font-size:13px; color:#506300;">⭐ {court["rating"]}</span>'
        f'</div>'
        f'<div style="font-size:12px; color:#3d4455; margin-top:4px;">📍 {court["location"]}</div>'
        f'<div style="margin-top:12px;">'
        f'<span class="eyebrow" style="font-size:9px;">STARTS AT</span><br/>'
        f'<span class="display" style="font-size:20px;">฿{court["price_per_hour"]}</span>'
        f'<span style="font-size:11px; color:#3d4455;"> /hr</span>'
        f'</div>'
        f'</div>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)

    if show_book:
        if st.button("Book Now", key=f"{key_prefix}_{court['id']}_book",
                     type="primary", width='stretch'):
            navigate("court_details", selected_court_id=court["id"])


def kpi_card(label, value, delta=None, icon=None):
    icon_html  = f'<span style="font-size:18px; display:block; margin-bottom:4px;">{icon}</span>' if icon else ""
    delta_html = f'<div style="font-size:12px; color:#2E6B00; margin-top:2px;">{delta}</div>' if delta else ""
    # NOTE: HTML must NOT be indented — markdown treats 4+ space indents as code blocks
    # and escapes the angle brackets, which is what makes raw <div> show up on the page.
    html = (
        f'<div class="kpi-card">'
        f'{icon_html}'
        f'<div class="eyebrow">{label}</div>'
        f'<div class="display" style="font-size:28px;">{value}</div>'
        f'{delta_html}'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


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
    # HTML must be unindented — markdown treats 4+ space indents as a code block
    # and escapes the angle brackets (same bug pattern as the old kpi_card).
    html = (
        f'<div class="zpots-card" style="display:flex; gap:20px; padding:20px; align-items:flex-start;">'
        f'<div style="width:180px; min-width:180px; height:120px; border-radius:12px;'
        f'background:linear-gradient(135deg,{booking["color"]},{booking["color"]}cc);'
        f'display:flex; align-items:center; justify-content:center; position:relative;">'
        f'<span style="font-size:2rem;">{SPORT_ICON.get(booking.get("sport", "Badminton"), "🏸")}</span>'
        f'{ai_badge}'
        f'</div>'
        f'<div style="flex:1;">'
        f'<div style="font-weight:700; font-size:18px; color:#1c2526;">{booking["court_name"]}</div>'
        f'<div style="display:flex; gap:20px; margin-top:8px; font-size:13px; color:#3d4455;">'
        f'<span>📅 {booking["date"]}</span>'
        f'<span>🕐 {booking["time_start"]} – {booking["time_end"]}</span>'
        f'</div>'
        f'<div style="margin-top:10px; display:flex; gap:6px; align-items:center;">'
        f'<span class="status-badge {status_cls}">{booking["status"]}</span>'
        f'<span style="font-size:12px; color:#3d4455;">Booking #{booking.get("id", "ZP-00000")}</span>'
        f'</div>'
        f'<div style="margin-top:10px;">{team_html}</div>'
        f'</div>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)

    if st.button("🎫 View QR", key=f"{key_prefix}_{booking['id']}_qr", type="primary"):
        navigate("checkin_qr", selected_booking_id=booking["id"])


def venue_card_owner(venue, key_prefix="ven"):
    # Compact layout: 36px coloured left rail instead of a 70px header block.
    st.markdown(f"""
    <div class="zpots-card" style="padding:0; overflow:hidden; display:flex;
                                    align-items:stretch; min-height:64px;">
        <div style="width:6px; background:linear-gradient(180deg,{venue['color']},{venue['color']}cc);"></div>
        <div style="padding:10px 14px; flex:1;">
            <div style="font-weight:600; font-size:13px; color:#1c2526;">{venue['name']}</div>
            <div class="eyebrow" style="font-size:9px; margin-top:2px;">{venue['location']}</div>
            <div style="display:flex; justify-content:space-between; margin-top:4px;
                        font-size:11px; color:#3d4455;">
                <span>{venue.get('courts_count',0)} courts</span>
                <span class="display" style="color:#2E6B00; font-size:13px;">
                    ฿{venue.get('revenue_today',0)}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Edit", key=f"{key_prefix}_{venue['id']}", width='stretch'):
        navigate("manage_courts")
