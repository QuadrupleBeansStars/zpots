# Sports Field Booking Platform - MVP Mockup

A Streamlit-based mockup demonstrating the end-to-end platform flow for a sports field booking system in Bangkok.

## Overview

This platform consists of two main interfaces:
- **B2B Field Manager Portal** - Web interface for field owners to manage their sports facilities
- **B2C Player App** - Mobile-optimized interface for players to discover and book matches

## Features

### Field Manager Portal (B2B)
1. **Login** - Access manager dashboard
2. **Dashboard** - View today's bookings, revenue, and upcoming matches
3. **Field Management** - Create and edit field information
4. **Schedule/Timetable** - Manage time slots (Available/Booked/Blocked)
5. **Pricing** - Configure off-peak, peak, and weekend pricing
6. **Bookings** - View all bookings in one place

### Player App (B2C)
1. **Splash/Login** - Entry point for players
2. **Home Screen** - Discover nearby matches in Bangkok locations
3. **Match Detail** - View match information and joined players
4. **Booking Confirmation** - Confirm booking with field details

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Running the App

Start the Streamlit app:
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Usage

### Demo Flow - Field Manager
1. Switch to "Field Manager Portal (B2B)" tab
2. Click "Login to Dashboard" (no credentials needed)
3. Navigate through:
   - Dashboard: View bookings and revenue
   - Fields: Create/edit field information
   - Schedule: Manage time slots
   - Pricing: Set pricing rules
   - Bookings: View all bookings

### Demo Flow - Player
1. Switch to "Player App (B2C)" tab
2. Click "Login" or "Create Account"
3. Browse available matches at Bangkok locations
4. Click "View Match" on any match
5. Click "Join Match" to book
6. See booking confirmation

## Technical Details

- **Framework**: Streamlit
- **Data**: Hardcoded dummy data (no database)
- **Authentication**: Session state only (no real auth)
- **Payments**: Not implemented (mockup only)

## Bangkok Locations Featured

- Bangna Football Arena
- Rama 9 Sports Center
- Ladprao Futsal Hub
- Sukhumvit Arena

## Notes

This is a **mockup prototype** for demonstration purposes only. It includes:
- Static data
- No backend logic
- No payment integration
- Simple navigation flow

The goal is to visualize the user journey from field creation to player booking.
