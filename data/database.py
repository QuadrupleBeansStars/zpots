"""SQLite persistence layer for ZPOTS."""
import sqlite3
import hashlib
import secrets
from datetime import date, timedelta

import streamlit as st

DB_PATH = "zpots.db"


@st.cache_resource
def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db() -> None:
    conn = get_connection()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            email         TEXT    NOT NULL UNIQUE,
            name          TEXT    NOT NULL,
            password_hash TEXT    NOT NULL,
            salt          TEXT    NOT NULL,
            role          TEXT    NOT NULL DEFAULT 'player',
            created_at    TEXT    NOT NULL DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS bookings (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            txn_id      TEXT    NOT NULL UNIQUE,
            player_id   INTEGER NOT NULL REFERENCES users(id),
            player_name TEXT    NOT NULL,
            court_id    TEXT    NOT NULL,
            court_name  TEXT    NOT NULL,
            date        TEXT    NOT NULL,
            time_start  TEXT    NOT NULL,
            time_end    TEXT    NOT NULL,
            duration    INTEGER NOT NULL,
            total_price INTEGER NOT NULL,
            status      TEXT    NOT NULL DEFAULT 'CONFIRMED',
            created_at  TEXT    NOT NULL DEFAULT (datetime('now'))
        );

        CREATE INDEX IF NOT EXISTS idx_bookings_player ON bookings(player_id);
        CREATE INDEX IF NOT EXISTS idx_bookings_court  ON bookings(court_id, date);
    """)
    conn.commit()

    row = conn.execute("SELECT COUNT(*) FROM users").fetchone()
    if row[0] == 0:
        _seed(conn)


def _seed(conn: sqlite3.Connection) -> None:
    users = [
        ("player@zpots.ai",  "Alex Siriwan",    "demo123",  "player"),
        ("player2@zpots.ai", "Narin Kositchai", "demo123",  "player"),
        ("owner@zpots.ai",   "Venue Admin",     "owner123", "owner"),
    ]
    for email, name, pw, role in users:
        salt = secrets.token_hex(16)
        pw_hash = _hash_password(pw, salt)
        conn.execute(
            "INSERT INTO users (email, name, password_hash, salt, role) VALUES (?,?,?,?,?)",
            (email, name, pw_hash, salt, role),
        )
    conn.commit()

    player1 = conn.execute("SELECT id FROM users WHERE email=?", ("player@zpots.ai",)).fetchone()["id"]
    player2 = conn.execute("SELECT id FROM users WHERE email=?", ("player2@zpots.ai",)).fetchone()["id"]

    today = date.today()
    historical = [
        (player1, "Alex Siriwan",    "bbc-01", "Bangkok Badminton Center", (today - timedelta(days=10)).isoformat(), "18:00", "20:00", 2, 545),
        (player1, "Alex Siriwan",    "pdl-04", "Padel House Sukhumvit",    (today - timedelta(days=5)).isoformat(),  "07:00", "08:00", 1, 825),
        (player2, "Narin Kositchai", "sky-02", "Skyline Arena Football",   (today - timedelta(days=3)).isoformat(),  "20:00", "22:00", 2, 1480),
    ]
    for player_id, player_name, court_id, court_name, dt, ts, te, dur, price in historical:
        txn_id = f"ZP-{secrets.randbelow(90000) + 10000}"
        conn.execute(
            """INSERT OR IGNORE INTO bookings
               (txn_id, player_id, player_name, court_id, court_name, date, time_start, time_end, duration, total_price)
               VALUES (?,?,?,?,?,?,?,?,?,?)""",
            (txn_id, player_id, player_name, court_id, court_name, dt, ts, te, dur, price),
        )
    conn.commit()


# ── Auth ──────────────────────────────────────────────────────────────────────

def _hash_password(password: str, salt: str) -> str:
    return hashlib.sha256((salt + password).encode()).hexdigest()


def create_user(email: str, name: str, password: str, role: str = "player") -> dict | None:
    conn = get_connection()
    if conn.execute("SELECT 1 FROM users WHERE email=?", (email,)).fetchone():
        return None
    salt = secrets.token_hex(16)
    pw_hash = _hash_password(password, salt)
    conn.execute(
        "INSERT INTO users (email, name, password_hash, salt, role) VALUES (?,?,?,?,?)",
        (email, name, pw_hash, salt, role),
    )
    conn.commit()
    return dict(conn.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone())


def get_user_by_email(email: str) -> dict | None:
    row = get_connection().execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
    return dict(row) if row else None


def verify_password(user: dict, password: str) -> bool:
    return _hash_password(password, user["salt"]) == user["password_hash"]


# ── Bookings ──────────────────────────────────────────────────────────────────

def create_booking(
    player_id: int,
    player_name: str,
    court_id: str,
    court_name: str,
    date_iso: str,
    time_start: str,
    time_end: str,
    duration: int,
    total_price: int,
) -> str:
    conn = get_connection()
    txn_id = f"ZP-{secrets.randbelow(90000) + 10000}"
    conn.execute(
        """INSERT INTO bookings
           (txn_id, player_id, player_name, court_id, court_name, date, time_start, time_end, duration, total_price)
           VALUES (?,?,?,?,?,?,?,?,?,?)""",
        (txn_id, player_id, player_name, court_id, court_name, date_iso, time_start, time_end, duration, total_price),
    )
    conn.commit()
    return txn_id


def get_bookings_by_user(player_id: int) -> list[dict]:
    rows = get_connection().execute(
        "SELECT * FROM bookings WHERE player_id=? ORDER BY created_at DESC",
        (player_id,),
    ).fetchall()
    return [dict(r) for r in rows]


def get_booked_slots(court_id: str, date_iso: str) -> set[str]:
    """Return set of time_start strings that are consumed (including multi-hour spans)."""
    rows = get_connection().execute(
        "SELECT time_start, duration FROM bookings WHERE court_id=? AND date=? AND status!='CANCELLED'",
        (court_id, date_iso),
    ).fetchall()
    booked: set[str] = set()
    for row in rows:
        start_h = int(row["time_start"].split(":")[0])
        for offset in range(row["duration"]):
            booked.add(f"{start_h + offset:02d}:00")
    return booked


def get_all_bookings() -> list[dict]:
    rows = get_connection().execute(
        "SELECT * FROM bookings ORDER BY created_at DESC"
    ).fetchall()
    return [dict(r) for r in rows]


def cancel_booking(booking_id: int, player_id: int) -> bool:
    """Mark a booking CANCELLED. Returns True iff the booking exists AND belongs to player_id."""
    conn = get_connection()
    cur = conn.execute(
        "UPDATE bookings SET status='CANCELLED' WHERE id=? AND player_id=? AND status!='CANCELLED'",
        (booking_id, player_id),
    )
    conn.commit()
    return cur.rowcount == 1
