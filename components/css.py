"""ZPOTS Design System - Kinetic Precision CSS."""
import streamlit as st


def inject_global_css():
    """Inject the full design system CSS."""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700&family=Lexend:wght@300;400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/icon?family=Material+Icons+Outlined');

    :root {
        --zpots-lime: #cffc00;
        --zpots-lime-dim: #c2ed00;
        --zpots-primary: #506300;
        --zpots-primary-dark: #4b5e00;
        --zpots-secondary: #615e00;
        --zpots-surface: #f6f6ff;
        --zpots-surface-low: #eef0ff;
        --zpots-surface-container: #e2e7ff;
        --zpots-surface-high: #d1dcff;
        --zpots-on-surface: #272e42;
        --zpots-on-surface-variant: #535b71;
        --zpots-outline: #6f768e;
        --zpots-outline-variant: #a5adc6;
        --zpots-inverse-surface: #060e20;
        --zpots-error: #b02500;
        --zpots-white: #ffffff;
    }

    /* Global font overrides */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
        color: var(--zpots-on-surface);
    }
    h1, h2, h3 {
        font-family: 'Space Grotesk', sans-serif !important;
        color: var(--zpots-on-surface) !important;
        letter-spacing: -0.02em;
    }
    h1 { font-weight: 700 !important; }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Main container adjustments */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        max-width: 1200px !important;
    }

    /* Primary button -> Electric Lime */
    .stButton > button[kind="primary"],
    .stButton > button[data-testid="baseButton-primary"] {
        background: linear-gradient(135deg, #cffc00, #c2ed00) !important;
        color: #4b5e00 !important;
        border: none !important;
        border-radius: 12px !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        padding: 0.6rem 1.5rem !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button[kind="primary"]:hover,
    .stButton > button[data-testid="baseButton-primary"]:hover {
        background: linear-gradient(135deg, #c2ed00, #b5de00) !important;
        transform: translateY(-1px);
    }

    /* Secondary button */
    .stButton > button[kind="secondary"],
    .stButton > button[data-testid="baseButton-secondary"] {
        background: var(--zpots-white) !important;
        color: var(--zpots-on-surface) !important;
        border: none !important;
        border-radius: 12px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        box-shadow: 0 2px 8px rgba(39,46,66,0.06) !important;
        padding: 0.6rem 1.5rem !important;
    }

    /* Default button styling */
    .stButton > button {
        border-radius: 12px !important;
        font-family: 'Inter', sans-serif !important;
        border: none !important;
        transition: all 0.2s ease !important;
    }

    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0px;
        background: var(--zpots-surface-low);
        border-radius: 12px;
        padding: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        padding: 8px 20px;
    }
    .stTabs [aria-selected="true"] {
        background: var(--zpots-white) !important;
        box-shadow: 0 2px 8px rgba(39,46,66,0.08);
    }
    .stTabs [data-baseweb="tab-highlight"] { display: none; }
    .stTabs [data-baseweb="tab-border"] { display: none; }

    /* Custom card classes */
    .zpots-card {
        background: var(--zpots-white);
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 8px 24px rgba(39,46,66,0.06);
    }
    .zpots-card-dark {
        background: var(--zpots-inverse-surface);
        border-radius: 16px;
        padding: 1.5rem;
        color: white;
    }
    .glass-card {
        background: rgba(255,255,255,0.85);
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 8px 24px rgba(39,46,66,0.08);
    }
    .zpots-card-lime {
        background: linear-gradient(135deg, #cffc00, #e8ff66);
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
        background: rgba(207,252,0,0.15);
        color: #506300;
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
    .status-confirmed { background: rgba(207,252,0,0.15); color: #506300; }
    .status-completed { background: rgba(80,99,0,0.1); color: #506300; }
    .status-cancelled { background: rgba(176,37,0,0.1); color: #b02500; }
    .status-booked { background: rgba(207,252,0,0.15); color: #506300; }
    .status-active { background: rgba(207,252,0,0.2); color: #506300; }
    .status-maintenance { background: rgba(255,165,0,0.15); color: #8a6500; }

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
        color: rgba(255,255,255,0.6);
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.2rem;
    }

    /* KPI card */
    .kpi-card {
        background: var(--zpots-white);
        border-radius: 16px;
        padding: 1.2rem;
        box-shadow: 0 4px 16px rgba(39,46,66,0.04);
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
        background: linear-gradient(135deg, #506300 0%, #789200 50%, #cffc00 100%);
        border-radius: 20px;
        padding: 2rem;
        color: white;
    }
    .revenue-banner h1 { color: white !important; }

    /* Star rating */
    .star-filled { color: #cffc00; font-size: 28px; }
    .star-empty { color: #d1dcff; font-size: 28px; }

    /* Chip / Filter chip */
    .chip {
        display: inline-block;
        padding: 6px 16px;
        border-radius: 999px;
        font-family: 'Inter', sans-serif;
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

    /* Dark login background */
    .dark-login-bg {
        background: linear-gradient(135deg, #060e20 0%, #1a2a3a 50%, #0a1a2a 100%);
        min-height: 100vh;
        padding: 2rem;
        margin: -1rem -1rem 0 -1rem;
    }

    /* Sidebar styling for owner */
    section[data-testid="stSidebar"] {
        background: var(--zpots-white) !important;
        border-right: none !important;
    }
    section[data-testid="stSidebar"] .stRadio label {
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        padding: 8px 16px !important;
        border-radius: 10px !important;
        transition: all 0.2s ease !important;
    }

    /* Input styling */
    .stTextInput input, .stSelectbox select, .stNumberInput input {
        border-radius: 12px !important;
        border: none !important;
        background: var(--zpots-surface-low) !important;
        font-family: 'Inter', sans-serif !important;
    }
    .stTextInput input:focus {
        background: var(--zpots-white) !important;
        box-shadow: 0 0 0 2px rgba(80,99,0,0.2) !important;
    }

    /* Toggle styling */
    .stToggle label span {
        font-family: 'Inter', sans-serif !important;
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

    /* Link styling */
    a { color: var(--zpots-primary) !important; text-decoration: none !important; }
    a:hover { color: var(--zpots-primary-dark) !important; }

    /* Horizontal rule replacement */
    hr {
        border: none;
        height: 1px;
        background: var(--zpots-surface-container);
        margin: 1.5rem 0;
    }

    /* Hide fullscreen button on images */
    button[title="View fullscreen"] { display: none !important; }

    /* Expander styling */
    .streamlit-expanderHeader {
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        border-radius: 12px !important;
    }
    </style>
    """, unsafe_allow_html=True)


def inject_login_css():
    """Additional CSS for login pages with dark backgrounds."""
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(160deg, #060e20 0%, #0d1b2e 40%, #162d3e 70%, #1a3040 100%) !important;
    }
    .stApp h1, .stApp h2, .stApp h3 {
        color: white !important;
    }
    .stApp p, .stApp label, .stApp span {
        color: rgba(255,255,255,0.8) !important;
    }
    .stTextInput label, .stTextInput input {
        color: var(--zpots-on-surface) !important;
    }
    .block-container {
        max-width: 1400px !important;
    }
    </style>
    """, unsafe_allow_html=True)


def inject_owner_sidebar_css():
    """Additional CSS for owner pages with sidebar."""
    st.markdown("""
    <style>
    section[data-testid="stSidebar"] {
        background: var(--zpots-white) !important;
        min-width: 240px !important;
        max-width: 240px !important;
    }
    </style>
    """, unsafe_allow_html=True)
