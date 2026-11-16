
import sqlite3
from pathlib import Path
from contextlib import contextmanager

# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Database file path
DATABASE_PATH = BASE_DIR / "travel.db"


@contextmanager
def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def initialize_database():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS trips (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                origin TEXT NOT NULL,
                destination TEXT NOT NULL,
                departure_date TEXT NOT NULL,
                return_date TEXT,
                travelers INTEGER NOT NULL,
                preferences TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

    print("Database initialized successfully!")


def create_trip(
    origin,
    destination,
    departure_date,
    return_date,
    travelers,
    preferences=None
):
    with get_connection() as connection:
        cursor = connection.execute("""
            INSERT INTO trips (
                origin,
                destination,
                departure_date,
                return_date,
                travelers,
                preferences
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            origin,
            destination,
            str(departure_date),
            str(return_date) if return_date else None,
            travelers,
            preferences
        ))

        return cursor.lastrowid


def get_all_trips():
    with get_connection() as connection:
        cursor = connection.execute(
            "SELECT * FROM trips ORDER BY id DESC"
        )

        return [dict(row) for row in cursor.fetchall()]


def get_trip_by_id(trip_id):
    with get_connection() as connection:
        cursor = connection.execute(
            "SELECT * FROM trips WHERE id = ?",
            (trip_id,)
        )

        row = cursor.fetchone()

        return dict(row) if row else None
