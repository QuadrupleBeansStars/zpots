"""AI Insights - Demand analysis and predictions."""
import streamlit as st
from components.css import inject_global_css
from components.nav import render_owner_sidebar


def render():
    inject_global_css()
    render_owner_sidebar()

    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("""
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:14px;">
            <h1 class="display" style="font-size:30px;">AI INSIGHTS</h1>
            <span class="status-badge status-active">ELITE VENUE PARTNER</span>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        if st.button("Generate AI Summary", type="primary", icon=":material/smart_toy:"):
            st.toast("AI summary generated!")
        st.button("Regenerate", key="ai_regen")

    # AI Summary Card
    st.markdown("""
    <div class="zpots-card" style="padding:20px;margin-bottom:18px;">
        <span class="ai-tag">AI GENERATED SUMMARY</span>
        <p style="margin-top:12px;line-height:1.6;font-size:14px;">
            Your Friday evening slots (18:00–21:00) continue to dominate revenue,
            driving <strong>41% of weekly bookings</strong>. Sukhumvit demand is saturated —
            consider opening Court 4 for tournament-rate pricing. Thong Lor traffic predicted
            to intensify Saturday after 16:00 due to weather;
            auto-rescheduling recommended for 12% of bookings.</p>
    </div>
    """, unsafe_allow_html=True)

    # Heatmap + Utilization row
    heat_col, util_col = st.columns([1.5, 1], gap="medium")

    with heat_col:
        st.markdown("""
        <div class="zpots-card" style="padding:20px;">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:12px;">
                <div>
                    <h3 class="display" style="font-size:16px;">Bangkok Demand Heatmap</h3>
                    <div class="eyebrow" style="margin-top:2px;">LIVE AI PROJECTION · NEXT 24 HOURS</div>
                </div>
                <div style="display:flex;gap:4px;">
                    <span class="status-badge status-cancelled">CRITICAL</span>
                    <span class="status-badge status-active">OPTIMAL</span>
                </div>
            </div>
            <div style="height:200px;background:radial-gradient(circle at 30% 40%,#CFFC00,transparent 40%),
                         radial-gradient(circle at 70% 60%,#FFDDCC,transparent 40%),
                         radial-gradient(circle at 50% 30%,#E2E7FF,transparent 40%),#F2F9EE;
                         border-radius:12px;display:flex;align-items:center;justify-content:center;">
                <span class="eyebrow">DEMAND DENSITY PROJECTION</span>
            </div>
            <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:12px;">
                <div class="zpots-card-surface" style="padding:14px;text-align:center;">
                    <div class="eyebrow" style="font-size:9px;">Sukhumvit</div>
                    <div class="display" style="font-size:22px;margin:4px 0;">94%</div>
                    <span class="status-badge" style="background:#CFFC00;color:#1E4A00;">Peak</span>
                </div>
                <div class="zpots-card-surface" style="padding:14px;text-align:center;">
                    <div class="eyebrow" style="font-size:9px;">Ari District</div>
                    <div class="display" style="font-size:22px;margin:4px 0;">62%</div>
                    <span class="status-badge status-progress">Moderate</span>
                </div>
                <div class="zpots-card-surface" style="padding:14px;text-align:center;">
                    <div class="eyebrow" style="font-size:9px;">Thong Lor</div>
                    <div class="display" style="font-size:22px;margin:4px 0;">98%</div>
                    <span class="status-badge status-cancelled">Saturated</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with util_col:
        st.markdown("""
        <div class="zpots-card" style="padding:18px;margin-bottom:10px;">
            <h3 class="display" style="font-size:15px;">Peak Utilization</h3>
            <div class="eyebrow" style="margin-top:2px;">HOURLY DISTRIBUTION</div>
            <div style="display:flex;align-items:flex-end;gap:3px;height:100px;margin-top:12px;">
        """ + "".join(
            f'<div style="flex:1;height:{v}%;background:'
            f'{"#CFFC00" if v>80 else "#2E6B00" if v>50 else "#A5D6A7"};'
            f'border-radius:3px 3px 0 0;"></div>'
            for v in [30,35,38,42,50,58,62,68,75,85,92,95,88,70,50,30]
        ) + """
            </div>
        </div>
        <div class="zpots-card" style="padding:18px;">
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px;">
                <span style="color:#CFFC00;font-size:14px;text-shadow:0 0 8px #CFFC00;">⚡</span>
                <strong>Golden Slot</strong>
                <span style="color:#506300;font-weight:700;margin-left:auto;">฿2,400/hr</span>
            </div>
            <div style="font-size:12px;color:#3d4455;">19:00</div>
            <div style="height:1px;background:#E3F0DE;margin:10px 0;"></div>
            <div style="display:flex;align-items:center;gap:8px;font-size:12px;color:#3d4455;">
                ⏳ Off-Peak (14:00)
                <span style="font-weight:600;margin-left:auto;">฿1,200/hr</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)

    # No-Show Risk + Mitigation row
    risk_col, mit_col = st.columns(2, gap="medium")

    with risk_col:
        st.markdown("""
        <div class="zpots-card" style="padding:20px;">
            <h3 class="display" style="font-size:16px;">No-Show Risk Analysis ⚠️</h3>
            <div class="eyebrow" style="color:#b02500;margin-top:2px;">PRIORITY: HIGH INTERVENTION</div>
            <div class="zpots-card-surface" style="display:flex;justify-content:space-between;
                         align-items:center;padding:14px;margin-top:14px;">
                <span style="font-size:13px;">Probable No-Shows</span>
                <span class="display" style="font-size:16px;">12%
                    <span style="font-size:12px;color:#b02500;">(+4% WoW)</span></span>
            </div>
            <div class="zpots-card-surface" style="padding:14px;margin-top:8px;">
                <div class="eyebrow">PRIMARY ROOT CAUSE</div>
                <div style="font-size:13px;margin-top:4px;">
                    Traffic delays on Rama IV during rain predicted (70% probability).</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with mit_col:
        st.markdown("""
        <div class="zpots-card-surface" style="padding:20px;">
            <h3 class="display" style="font-size:16px;margin-bottom:12px;">
                AI Mitigation Strategies</h3>
            <div style="display:flex;gap:10px;">
                <div class="zpots-card" style="flex:1;padding:14px;">
                    <h4 style="font-size:13px;margin-bottom:4px;">Smart Reschedule</h4>
                    <p style="font-size:11px;color:#3d4455;line-height:1.5;">
                        Auto-offer 15-min delay window to users in high-traffic zones.</p>
                    <div class="eyebrow" style="color:#506300;font-size:8px;margin-top:8px;">
                        +23% RETENTION</div>
                </div>
                <div class="zpots-card" style="flex:1;padding:14px;">
                    <h4 style="font-size:13px;margin-bottom:4px;">Pre-Check Deposit</h4>
                    <p style="font-size:11px;color:#3d4455;line-height:1.5;">
                        20% commitment fee for high-demand Saturday slots.</p>
                    <div class="eyebrow" style="color:#506300;font-size:8px;margin-top:8px;">
                        -60% NO-SHOWS</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.button("Execute All", type="primary", key="execute_all_mit")
