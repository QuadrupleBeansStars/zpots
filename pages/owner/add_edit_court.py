"""Add/Edit Court - Multi-step form."""
import streamlit as st
import pandas as pd
from components.css import inject_global_css, inject_owner_sidebar_css
from components.nav import navigate, render_owner_sidebar
from data.dummy_data import COURTS, SPORTS_LIST


def render():
    inject_global_css()
    inject_owner_sidebar_css()
    render_owner_sidebar()

    court_id = st.session_state.get("editing_court_id")
    court = next((c for c in COURTS if c["id"] == court_id), None) if court_id else None
    is_edit = court is not None

    st.markdown(f'<div style="font-family:\'Lexend\'; font-size:10px; text-transform:uppercase; letter-spacing:0.1em; color:#535b71;">VENUES {"› EDIT COURT" if is_edit else "› NEW COURT"}</div>', unsafe_allow_html=True)
    st.markdown(f"# {'Edit: ' + court['name'] if is_edit else 'Add New Court'}")
    st.markdown('<p style="color:#535b71; font-size:14px;">Configure high-performance court settings. Changes reflect across all booking channels instantly through AI Sync.</p>', unsafe_allow_html=True)

    if "court_step" not in st.session_state:
        st.session_state.court_step = 0

    steps = ["BASICS", "SLOTS", "PRICING"]
    step_cols = st.columns(3)
    for i, step_name in enumerate(steps):
        with step_cols[i]:
            bg = "background:#cffc00; color:#4b5e00;" if st.session_state.court_step == i else "background:#eef0ff; color:#535b71;"
            st.markdown(f'<div style="text-align:center; padding:10px; border-radius:12px; {bg} font-family:\'Lexend\'; font-size:11px; font-weight:600; letter-spacing:0.08em;">0{i+1} &nbsp; {step_name}</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:1.5rem;'></div>", unsafe_allow_html=True)

    if st.session_state.court_step == 0:
        form_col, visual_col = st.columns([1.2, 1])
        with form_col:
            st.markdown('<h3 style="font-size:1rem;">⚙️ Court Fundamentals</h3>', unsafe_allow_html=True)
            st.text_input("COURT NAME", value=court["name"] if is_edit else "", key="court_name")
            cat_col, surf_col = st.columns(2)
            with cat_col:
                st.selectbox("SPORT CATEGORY", SPORTS_LIST, index=SPORTS_LIST.index(court["sport"]) if is_edit else 0, key="court_sport")
            with surf_col:
                st.selectbox("SURFACE TYPE", ["Professional Mat", "Premium Synthetic", "Artificial Turf", "Hardwood", "Indoor Acrylic"], key="court_surface")
            st.text_input("LOCATION / FULL ADDRESS", value=court["location"] if is_edit else "", key="court_location")

            st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)
            st.markdown('<h3 style="font-size:1rem;">⚡ Kinetic Amenities</h3>', unsafe_allow_html=True)
            amenities = ["AC Units", "Pro Lighting", "Locker Rooms", "Water Station", "AI Video", "Showers"]
            am_cols = st.columns(3)
            for i, am in enumerate(amenities):
                with am_cols[i % 3]:
                    st.checkbox(am, value=(i < 4) if is_edit else False, key=f"amenity_{i}")

        with visual_col:
            st.markdown('<div style="font-family:\'Lexend\'; font-size:10px; text-transform:uppercase; letter-spacing:0.1em; color:#535b71;">VISUAL ASSETS <span class="status-badge status-active" style="background:rgba(207,252,0,0.3); padding:2px 8px; border-radius:4px; font-size:9px;">REQUIRED</span></div>', unsafe_allow_html=True)
            color = court["color"] if is_edit else "#2a2a3a"
            st.markdown(f'<div class="court-image" style="background:linear-gradient(135deg, {color}, {color}cc); height:180px;"><span style="font-size:2rem;">📸</span></div>', unsafe_allow_html=True)
            st.file_uploader("Upload photos", type=["jpg", "png"], accept_multiple_files=True, key="court_photos", label_visibility="collapsed")

            st.markdown('<div style="font-family:\'Lexend\'; font-size:10px; text-transform:uppercase; letter-spacing:0.1em; color:#535b71; margin-top:1rem;">LOCATION MAPPING</div>', unsafe_allow_html=True)
            st.map(pd.DataFrame({"lat": [13.7367], "lon": [100.5232]}), zoom=13)

            st.markdown("""
            <div class="zpots-card" style="background:rgba(80,99,0,0.08); margin-top:1rem;">
                <div style="font-family:'Lexend'; font-size:10px; text-transform:uppercase; letter-spacing:0.1em; color:#506300;">AI OPTIMIZATION</div>
                <p style="font-size:12px; color:#535b71; margin-top:4px;">Courts with "Pro Lighting" and "Air Conditioning" amenities see 42% higher booking rates in the Bangkok region.</p>
            </div>
            """, unsafe_allow_html=True)

    elif st.session_state.court_step == 1:
        st.markdown("### Slot Configuration")
        st.markdown('<p style="color:#535b71;">Configure available time slots for this court.</p>', unsafe_allow_html=True)
        scol1, scol2 = st.columns(2)
        with scol1:
            st.time_input("Opening Time", value=None, key="slot_open")
            st.time_input("Closing Time", value=None, key="slot_close")
        with scol2:
            st.number_input("Slot Duration (minutes)", value=60, step=30, key="slot_duration")
            st.number_input("Buffer Between Slots (minutes)", value=15, step=5, key="slot_buffer")
        st.toggle("Enable AI Auto-Scheduling", value=True, key="ai_auto_schedule")

    elif st.session_state.court_step == 2:
        st.markdown("### Pricing Configuration")
        st.markdown('<p style="color:#535b71;">Set base rates and enable AI dynamic pricing.</p>', unsafe_allow_html=True)
        pcol1, pcol2 = st.columns(2)
        with pcol1:
            st.number_input("Standard Rate (THB/hr)", value=450, step=50, key="price_standard")
        with pcol2:
            st.number_input("Prime Time Rate (THB/hr)", value=650, step=50, key="price_prime")
        st.toggle("Enable AI Dynamic Pricing", value=True, key="ai_dynamic_pricing")
        st.slider("Price Flexibility Range", 0, 50, 20, format="%d%%", key="price_flex")

    st.markdown("<div style='height:1.5rem;'></div>", unsafe_allow_html=True)
    nav_cols = st.columns([1, 1, 1])
    with nav_cols[0]:
        if st.session_state.court_step > 0:
            if st.button("← Back", key="step_back"):
                st.session_state.court_step -= 1
                st.rerun()
        else:
            if st.button("Discard Changes", key="discard"):
                navigate("manage_courts")
    with nav_cols[2]:
        if st.session_state.court_step < 2:
            if st.button("Save & Continue →", type="primary", key="step_next", use_container_width=True):
                st.session_state.court_step += 1
                st.rerun()
        else:
            if st.button("Save Court →", type="primary", key="save_court", use_container_width=True):
                st.toast("Court saved successfully!")
                st.session_state.court_step = 0
                navigate("manage_courts")
