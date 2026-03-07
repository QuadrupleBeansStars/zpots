SYSTEM JOURNEY MOCKUP (MVP)
Context: Sports field booking platform in Bangkok, Thailand
Goal: Demonstrate the user journey through interface mockups (not technical requirements)

=========================================================
B2B JOURNEY — FIELD MANAGER WEB PORTAL
(Used by field owners / managers via web browser)
=========================================================

STEP 1 — LOGIN SCREEN

---------------------------------------------------------
|                     FIELD MANAGER                     |
|-------------------------------------------------------|
| Email:     [________________________]                 |
| Password:  [________________________]                 |
|                                                       |
|                [ Login to Dashboard ]                 |
|                                                       |
| Forgot password?                                     |
---------------------------------------------------------

Manager logs into the backend system.



STEP 2 — DASHBOARD

---------------------------------------------------------
| Dashboard | Fields | Schedule | Pricing | Bookings    |
---------------------------------------------------------
|                                                   |
|  Today's Summary                                 |
|  ---------------------------------------------    |
|  Total Bookings Today: 12                        |
|  Revenue Today: ฿7,800                           |
|                                                   |
|  Upcoming Bookings                               |
|  ---------------------------------------------    |
|  18:00  Team A vs Team B                         |
|  19:00  Casual Match                             |
|  20:00  Corporate Booking                        |
|                                                   |
|                     [ Manage Fields ]             |
---------------------------------------------------------

Manager can navigate to field configuration.



STEP 3 — CREATE / EDIT FIELD

---------------------------------------------------------
| Add New Field                                       |
---------------------------------------------------------
| Field Name:                                         |
| [ Bangna Football Arena ]                           |
|                                                     |
| Description:                                        |
| [ Indoor futsal field with parking and showers ]    |
|                                                     |
| Upload Images                                       |
| [ Upload ] [ Upload ] [ Upload ]                    |
|                                                     |
| Location                                            |
| [ Google Map Pin — Bangkok ]                        |
|                                                     |
| Address:                                            |
| Bangna-Trad Rd, Bangna, Bangkok                     |
|                                                     |
|                     [ Save Field ]                  |
---------------------------------------------------------

Manager sets field information.



STEP 4 — SCHEDULE MANAGEMENT (TIMETABLE)

---------------------------------------------------------
| Schedule — Bangna Football Arena                     |
| Date: 12 July 2026                                   |
---------------------------------------------------------
| Time     | Status                                   |
|-----------------------------------------------------|
| 08:00    | Available                                |
| 09:00    | Available                                |
| 10:00    | Maintenance (Blocked)                    |
| 11:00    | Available                                |
| 12:00    | Available                                |
| 13:00    | Available                                |
| 14:00    | Booked                                   |
| 15:00    | Booked                                   |
| 16:00    | Available                                |
| 17:00    | Available                                |
| 18:00    | Available                                |
| 19:00    | Available                                |
| 20:00    | Available                                |
---------------------------------------------------------

Manager can:
- Click a slot to block it
- Enable booking
- View booking details



STEP 5 — PRICING MANAGEMENT

---------------------------------------------------------
| Pricing Settings                                    |
---------------------------------------------------------
| Off-Peak Price                                      |
| 08:00 - 16:00                                       |
| Price per hour:  ฿1,000                             |
|                                                     |
| Peak Price                                          |
| 17:00 - 22:00                                       |
| Price per hour:  ฿1,500                             |
|                                                     |
| Weekend Price                                       |
| Price per hour:  ฿1,800                             |
|                                                     |
|                    [ Save Pricing ]                 |
---------------------------------------------------------

Manager defines booking prices.



STEP 6 — BOOKINGS VIEW

---------------------------------------------------------
| Bookings — Today                                    |
---------------------------------------------------------
| Time   | Player Name | Status                       |
|-----------------------------------------------------|
| 14:00  | Team Somchai | Confirmed                   |
| 15:00  | Office Team  | Confirmed                   |
| 18:00  | Open Match   | Available                   |
| 19:00  | Open Match   | Available                   |
---------------------------------------------------------

Manager monitors bookings from players.



STEP 7 — BOOKING NOTIFICATION

---------------------------------------------------------
| 🔔 New Booking                                      |
---------------------------------------------------------
| Field: Bangna Football Arena                        |
| Time: 19:00                                         |
| Player: Narin S.                                    |
|                                                     |
|              [ View Booking ]                       |
---------------------------------------------------------

Manager receives real-time notification.



=========================================================
B2C JOURNEY — PLAYER MOBILE APP
(Used by players on mobile phones)
=========================================================

STEP 1 — SPLASH SCREEN

---------------------------------------------------------
|                                                     |
|               PLAYMATCH BANGKOK                     |
|                                                     |
|        Find football games near you                |
|                                                     |
|                   [ Login ]                         |
|                 [ Create Account ]                  |
---------------------------------------------------------

User opens the app.



STEP 2 — HOME SCREEN

---------------------------------------------------------
| 📍 Bangkok                                          |
---------------------------------------------------------
| Nearby Matches                                      |
|-----------------------------------------------------|
| ⚽ Bangna Arena                                      |
| Today 19:00                                         |
| 5v5 Football                                        |
| Players Joined: 6 / 10                              |
| Price: ฿150                                         |
|                             [ View Match ]          |
|                                                     |
| ⚽ Rama 9 Sports Center                              |
| Today 20:00                                         |
| Players Joined: 4 / 10                              |
| Price: ฿120                                         |
|                             [ View Match ]          |
---------------------------------------------------------

User browses available matches.



STEP 3 — MATCH DETAILS

---------------------------------------------------------
| Bangna Football Arena                               |
---------------------------------------------------------
| Time: 19:00 - 20:00                                 |
| Format: 5v5                                         |
| Price: ฿150                                         |
|                                                     |
| Players Joined                                      |
|-----------------------------------------------------|
| Somchai                                             |
| Narin                                               |
| Krit                                                |
| Ball                                                |
|                                                     |
| Remaining Slots: 6                                  |
|                                                     |
|                 [ Join Match ]                      |
---------------------------------------------------------

User reviews match details.



STEP 4 — BOOK MATCH

---------------------------------------------------------
| Confirm Booking                                     |
---------------------------------------------------------
| Match: Bangna Football Arena                        |
| Time: 19:00                                         |
| Price: ฿150                                         |
|                                                     |
| Payment Method                                      |
| PromptPay / Credit Card                             |
|                                                     |
|                 [ Confirm Booking ]                 |
---------------------------------------------------------

User books a slot.



STEP 5 — BOOKING CONFIRMATION

---------------------------------------------------------
| 🎉 Booking Confirmed                                |
---------------------------------------------------------
| Match: Bangna Football Arena                        |
| Time: 19:00                                         |
|                                                     |
| Address                                             |
| Bangna-Trad Rd, Bangkok                             |
|                                                     |
|           [ Open Map ]  [ View Booking ]            |
---------------------------------------------------------

User receives booking confirmation.



=========================================================
END OF MVP USER JOURNEY
=========================================================

B2B: Manager configures field, schedule, and pricing.
B2C: Players discover matches and book available slots.