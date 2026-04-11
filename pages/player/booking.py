"""Booking Page - Secure Checkout."""
import streamlit as st
from components.css import inject_global_css
from components.nav import navigate, render_player_topbar
from data.dummy_data import COURTS


def render():
    inject_global_css()
    render_player_topbar()

    court = st.session_state.get("booking_court", COURTS[0])
    slot = st.session_state.get("booking_slot")
    if slot is None:
        st.warning("No time slot selected. Please go back and choose a slot.")
        if st.button("← Back to Court", key="back_to_court"):
            navigate("court_details")
        return


    st.markdown("""
    <div style="display:flex; align-items:center; gap:8px; margin-bottom:1rem;">
        <span style="font-size:18px; cursor:pointer;">←</span>
        <span style="font-family:'Lexend'; font-size:11px; text-transform:uppercase; letter-spacing:0.1em; color:#3d4455;">SECURE CHECKOUT</span>
    </div>
    """, unsafe_allow_html=True)

    left_col, right_col = st.columns([1, 1])

    with left_col:
        st.markdown(f"""
        <div class="court-image" style="background:linear-gradient(to bottom, {court['color']}cc, {court['color']}); height:200px; position:relative;">
            <div style="position:absolute; bottom:16px; left:16px;">
                <div style="font-family:'Space Grotesk'; font-weight:700; font-size:1.4rem; color:white;">{court['name']}</div>
                <div style="display:flex; align-items:center; gap:6px; margin-top:4px;">
                    <span style="color:#cffc00; font-size:12px;">●</span>
                    <span style="color:rgba(255,255,255,0.8); font-size:13px;">{court['location'].split(',')[0]}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:1.5rem;'></div>", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="zpots-card-surface">
            <div style="font-family:'Lexend'; font-size:10px; text-transform:uppercase; letter-spacing:0.1em; color:#3d4455; margin-bottom:8px;">SELECTED SESSION</div>
            <div style="font-family:'Inter'; font-weight:700; font-size:18px; color:#272e42;">Court 01 | Mon, 12th Nov</div>
            <div style="display:flex; gap:1.5rem; margin-top:8px;">
                <span style="font-size:13px; color:#3d4455;">🕐 {slot['time_start']} - {slot['time_end']}</span>
                <span style="font-size:13px; color:#3d4455;">⏱ 120 Minutes</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:1.5rem;'></div>", unsafe_allow_html=True)

        st.markdown("<h3 style='font-size:1rem;'>Payment Method</h3>", unsafe_allow_html=True)
        payment = st.radio(
            "Select payment",
            ["💳 Credit/Debit — Visa, Mastercard, JCB", "🏦 PromptPay — Local Thai Transfer", "📱 Apple Pay — Express Checkout"],
            key="payment_method",
            label_visibility="collapsed",
        )

    with right_col:
        base_price = slot["price"] * 2
        discount = 80
        service_fee = 25
        total = base_price - discount + service_fee

        st.markdown(f"""
        <div class="zpots-card">
            <h3 style="font-size:1.1rem; margin-bottom:1rem;">Summary</h3>
            <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
                <span style="font-size:14px; color:#3d4455;">Base price (2 hrs)</span>
                <span style="font-family:'Inter'; font-weight:500;">฿{base_price:.2f}</span>
            </div>
            <div style="display:flex; justify-content:space-between; margin-bottom:8px; align-items:center;">
                <span style="font-size:14px; color:#3d4455;">Dynamic Discount <span class="ai-tag" style="font-size:8px;">AI APPLIED</span></span>
                <span style="font-family:'Inter'; font-weight:500; color:#506300;">- ฿{discount:.2f}</span>
            </div>
            <div style="display:flex; justify-content:space-between; margin-bottom:12px;">
                <span style="font-size:14px; color:#3d4455;">Service Fee</span>
                <span style="font-family:'Inter'; font-weight:500;">฿{service_fee:.2f}</span>
            </div>
            <hr>
            <div style="font-family:'Lexend'; font-size:10px; text-transform:uppercase; letter-spacing:0.1em; color:#3d4455; margin-top:12px;">TOTAL AMOUNT</div>
            <div style="font-family:'Space Grotesk'; font-weight:700; font-size:2.5rem; color:#272e42;">฿{total:.2f}</div>
            <div style="font-size:11px; color:#3d4455; margin-bottom:1rem;">includes taxes & fees</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Confirm & Pay →", type="primary", width='stretch', key="confirm_pay"):
            st.session_state.booking_total_final = total
            navigate("booking_confirmation")

        st.markdown('<div style="text-align:center; font-size:11px; color:#3d4455; margin-top:8px;">🔒 BANK-GRADE ENCRYPTED</div>', unsafe_allow_html=True)

        st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)

        st.markdown("""
        <div class="zpots-card-surface" style="padding:1.2rem;">
            <span class="ai-tag" style="font-size:9px;">ZPOTS AI SUGGESTION</span>
            <p style="font-size:13px; color:#3d4455; font-style:italic; margin-top:8px;">"This time slot is typically quieter. You'll likely have more space for warm-ups on Court 01."</p>
        </div>
        """, unsafe_allow_html=True)
