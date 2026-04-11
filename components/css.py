"""ZPOTS Design System - Sports Theme CSS."""
import streamlit as st


def inject_global_css():
    """Inject the full design system CSS."""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@300;400;500;600;700&family=Lexend:wght@300;400;500;600;700&display=swap');

    :root {
        --zpots-lime: #cffc00;
        --zpots-lime-dim: #b8e000;
        --zpots-primary: #2e6b00;
        --zpots-primary-dark: #1e4a00;
        --zpots-surface: #ffffff;
        --zpots-surface-low: #f2f9ee;
        --zpots-surface-container: #e3f0de;
        --zpots-surface-high: #cde3c7;
        --zpots-on-surface: #1c2526;
        --zpots-on-surface-variant: #3d5040;
        --zpots-outline: #6f8a6e;
        --zpots-outline-variant: #a8c4a5;
        --zpots-inverse-surface: #0d1f0d;
        --zpots-error: #c62828;
        --zpots-white: #ffffff;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Main container */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        max-width: 1200px !important;
    }

    /* Primary button — Electric Lime brand */
    .stButton > button[kind="primary"],
    .stButton > button[data-testid="baseButton-primary"] {
        background: linear-gradient(135deg, #cffc00, #b8e000) !important;
        color: #1e4a00 !important;
        border: none !important;
        font-weight: 700 !important;
        letter-spacing: 0.03em !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button[kind="primary"]:hover,
    .stButton > button[data-testid="baseButton-primary"]:hover {
        background: linear-gradient(135deg, #b8e000, #a6cc00) !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(207,252,0,0.35) !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0px;
        background: var(--zpots-surface-low);
        border-radius: 12px;
        padding: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        font-weight: 500;
        padding: 8px 20px;
    }
    .stTabs [aria-selected="true"] {
        background: var(--zpots-white) !important;
        box-shadow: 0 2px 8px rgba(28,37,38,0.08);
    }
    .stTabs [data-baseweb="tab-highlight"] { display: none; }
    .stTabs [data-baseweb="tab-border"] { display: none; }

    /* Custom card classes */
    .zpots-card {
        background: var(--zpots-white);
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 16px rgba(28,37,38,0.06);
    }
    .zpots-card-dark {
        background: var(--zpots-inverse-surface);
        border-radius: 16px;
        padding: 1.5rem;
        color: white;
    }
    .glass-card {
        background: rgba(255,255,255,0.92);
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 8px 24px rgba(28,37,38,0.08);
    }
    .zpots-card-lime {
        background: linear-gradient(135deg, #cffc00, #e4ff7a);
        border-radius: 16px;
        padding: 1.5rem;
    }
    .zpots-card-surface {
        background: var(--zpots-surface-low);
        border-radius: 16px;
        padding: 1.5rem;
    }

    /* Tags */
    .ai-tag {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(207,252,0,0.18);
        color: #2e6b00;
        padding: 4px 12px;
        border-radius: 999px;
        font-family: 'Lexend', sans-serif;
        font-size: 10px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    .ai-tag::before {
        content: '';
        width: 6px;
        height: 6px;
        background: #cffc00;
        border-radius: 50%;
        box-shadow: 0 0 8px #cffc00;
    }

    /* Status colors */
    .status-confirmed { background: rgba(207,252,0,0.18); color: #2e6b00; }
    .status-completed { background: rgba(46,107,0,0.12); color: #2e6b00; }
    .status-cancelled { background: rgba(198,40,40,0.1); color: #c62828; }
    .status-booked { background: rgba(207,252,0,0.18); color: #2e6b00; }
    .status-active { background: rgba(207,252,0,0.22); color: #2e6b00; }
    .status-maintenance { background: rgba(230,81,0,0.12); color: #e65100; }

    .status-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 999px;
        font-family: 'Lexend', sans-serif;
        font-size: 10px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    /* Court image placeholder */
    .court-image {
        border-radius: 16px;
        overflow: hidden;
        position: relative;
        aspect-ratio: 16/10;
        display: flex;
        align-items: center;
        justify-content: center;
        color: rgba(255,255,255,0.75);
        font-size: 1.2rem;
    }

    /* KPI card */
    .kpi-card {
        background: var(--zpots-white);
        border-radius: 16px;
        padding: 1.2rem;
        box-shadow: 0 2px 12px rgba(28,37,38,0.05);
        border: 1px solid var(--zpots-surface-container);
    }
    .kpi-value {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        color: var(--zpots-on-surface);
        line-height: 1.1;
    }
    .kpi-label {
        font-family: 'Lexend', sans-serif;
        font-size: 10px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: var(--zpots-on-surface-variant);
        margin-bottom: 4px;
    }
    .kpi-delta {
        font-family: 'Inter', sans-serif;
        font-size: 12px;
        color: var(--zpots-primary);
    }

    /* Revenue banner */
    .revenue-banner {
        background: linear-gradient(135deg, #1e4a00 0%, #2e6b00 50%, #cffc00 100%);
        border-radius: 20px;
        padding: 2rem;
        color: white;
    }
    .revenue-banner h1, .revenue-banner h2 { color: white !important; }

    /* Star rating */
    .star-filled { color: #cffc00; font-size: 28px; }
    .star-empty { color: #c4dcc0; font-size: 28px; }

    /* Chip / Filter chip */
    .chip {
        display: inline-block;
        padding: 6px 16px;
        border-radius: 999px;
        font-size: 13px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    .chip-default {
        background: var(--zpots-surface-low);
        color: var(--zpots-on-surface);
    }
    .chip-selected {
        background: var(--zpots-lime);
        color: var(--zpots-primary-dark);
    }

    /* Metric override */
    [data-testid="stMetricValue"] {
        font-family: 'Space Grotesk', sans-serif !important;
    }
    [data-testid="stMetricLabel"] {
        font-family: 'Lexend', sans-serif !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
    }

    /* Horizontal rule */
    hr {
        border: none;
        height: 1px;
        background: var(--zpots-surface-container);
        margin: 1.5rem 0;
    }

    /* Hide fullscreen button on images */
    button[title="View fullscreen"] { display: none !important; }
    </style>
    """, unsafe_allow_html=True)


def inject_login_css():
    """Additional CSS for login pages with dark backgrounds."""
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(160deg, #060e20 0%, #0d1b2e 40%, #162d3e 70%, #1a3040 100%) !important;
    }
    /* Default: white text for dark background */
    .stApp h1, .stApp h2, .stApp h3 {
        color: white !important;
    }
    .stApp p, .stApp label, .stApp span {
        color: rgba(255,255,255,0.85) !important;
    }
    /* Glass card overrides — dark text on white card */
    .glass-card h1, .glass-card h2, .glass-card h3 {
        color: #272e42 !important;
    }
    .glass-card p, .glass-card span {
        color: #3d4455 !important;
    }
    /* Input fields always use dark text */
    .stTextInput label {
        color: rgba(255,255,255,0.9) !important;
        font-family: 'Lexend', sans-serif !important;
        font-size: 11px !important;
        letter-spacing: 0.08em !important;
    }
    .stTextInput input {
        color: var(--zpots-on-surface) !important;
    }
    .block-container {
        max-width: 1400px !important;
    }
    </style>
    """, unsafe_allow_html=True)


def inject_owner_sidebar_css():
    """Additional CSS for owner pages — dark sidebar with fixed width."""
    st.markdown("""
    <style>
    section[data-testid="stSidebar"] {
        min-width: 248px !important;
        max-width: 248px !important;
    }
    section[data-testid="stSidebar"] .stButton > button {
        text-align: left !important;
        justify-content: flex-start !important;
    }
    </style>
    """, unsafe_allow_html=True)
