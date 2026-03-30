"""Check-in QR Code Screen."""
import streamlit as st
from components.css import inject_global_css
from components.nav import navigate, render_player_topbar
from data.dummy_data import PLAYER_BOOKINGS

try:
    import qrcode
    from io import BytesIO
    HAS_QRCODE = True
except ImportError:
    HAS_QRCODE = False


def render():
    inject_global_css()
    render_player_topbar()

    booking_id = st.session_state.get("selected_booking_id", "ZP-94821")
    booking = next((b for b in PLAYER_BOOKINGS if b["id"] == booking_id), PLAYER_BOOKINGS[0])

    st.markdown('<span class="ai-tag">ACTIVE SESSION</span>', unsafe_allow_html=True)
    st.markdown("""
    <h1 style="font-size:3rem; line-height:1.05; margin:0.5rem 0;">READY TO<br><span style="color:#506300; font-style:italic;">PLAY.</span></h1>
    <p style="font-size:15px; color:#535b71; max-width:500px;">Your court is reserved and the AI has prepped the surface. Just scan and start.</p>
    """, unsafe_allow_html=True)

    left_col, right_col = st.columns([1, 1])

    with left_col:
        st.markdown("""
        <div class="zpots-card-surface" style="margin-top:1rem; display:flex; align-items:center; gap:12px;">
            <span style="font-size:1.2rem;">📋</span>
            <div>
                <div style="font-family:'Lexend'; font-size:10px; text-transform:uppercase; letter-spacing:0.1em; color:#535b71;">INSTRUCTIONS</div>
                <div style="font-size:13px; color:#272e42;">Scan this at the front desk to check-in.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with right_col:
        st.markdown('<div class="zpots-card" style="text-align:center; padding:2rem;">', unsafe_allow_html=True)
        if HAS_QRCODE:
            qr = qrcode.QRCode(version=1, box_size=8, border=2)
            qr.add_data(f"ZPOTS-CHECKIN-{booking['qr_code']}")
            qr.make(fit=True)
            img = qr.make_image(fill_color="#272e42", back_color="#ffffff")
            buf = BytesIO()
            img.save(buf, format="PNG")
            st.image(buf.getvalue(), width=200)
        else:
            st.markdown('<div style="width:200px; height:200px; margin:0 auto; background:#eef0ff; border-radius:12px; display:flex; align-items:center; justify-content:center; font-size:3rem;">📱</div>', unsafe_allow_html=True)

        st.markdown(f"""
            <div style="font-family:'Space Grotesk'; font-weight:700; font-size:1.3rem; margin-top:12px;">{booking['qr_code']}</div>
            <div style="font-size:12px; color:#535b71;">Valid for next 15 minutes</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:1.5rem;'></div>", unsafe_allow_html=True)

    info_cols = st.columns(3)
    with info_cols[0]:
        st.markdown(f"""
        <div class="zpots-card" style="text-align:center;">
            <div style="font-family:'Lexend'; font-size:9px; text-transform:uppercase; letter-spacing:0.1em; color:#535b71;">VENUE</div>
            <div style="font-family:'Inter'; font-weight:600; font-size:14px; margin-top:4px;">{booking['court_name']}</div>
            <div style="font-size:12px; color:#535b71;">Court {booking['court_number']} • {booking['surface']}</div>
        </div>
        """, unsafe_allow_html=True)
    with info_cols[1]:
        st.markdown(f"""
        <div class="zpots-card" style="text-align:center;">
            <div style="font-family:'Lexend'; font-size:9px; text-transform:uppercase; letter-spacing:0.1em; color:#535b71;">SCHEDULE</div>
            <div style="font-family:'Inter'; font-weight:600; font-size:14px; margin-top:4px;">Today, {booking['time_start']}</div>
            <div style="font-size:12px; color:#535b71;">{booking['duration_min']} Minute Session</div>
        </div>
        """, unsafe_allow_html=True)
    with info_cols[2]:
        st.markdown("""
        <div class="zpots-card" style="text-align:center;">
            <div style="font-family:'Lexend'; font-size:9px; text-transform:uppercase; letter-spacing:0.1em; color:#535b71;">STATUS</div>
            <div style="font-family:'Inter'; font-weight:600; font-size:14px; margin-top:4px; color:#506300;">Ready</div>
            <div style="font-size:12px; color:#535b71;">Court is prepared</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)
    loc_col1, loc_col2 = st.columns([3, 1])
    with loc_col1:
        st.markdown(f"""
        <div class="zpots-card-lime" style="display:flex; align-items:center; gap:12px;">
            <span style="font-size:1.3rem;">📍</span>
            <div>
                <div style="font-family:'Lexend'; font-size:10px; text-transform:uppercase; letter-spacing:0.1em; color:#4b5e00;">LOCATION</div>
                <div style="font-family:'Inter'; font-weight:600; font-size:14px; color:#4b5e00;">{booking['address']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with loc_col2:
        st.button("📍 Get Directions", type="primary", key="get_directions", use_container_width=True)

    st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)
    if st.button("← Back to My Bookings", key="back_bookings"):
        navigate("my_bookings")
