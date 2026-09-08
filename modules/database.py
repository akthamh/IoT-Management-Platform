import sqlite3
from pathlib import Path


# Absolute path to the project directory.
PROJECT_DIRECTORY = Path(__file__).resolve().parent.parent

# Runtime database files are stored inside the data directory.
DATA_DIRECTORY = PROJECT_DIRECTORY / "data"
DATABASE_PATH = DATA_DIRECTORY / "iot_platform.db"


def get_database_connection() -> sqlite3.Connection:
    """Create and return a connection to the SQLite database."""

    # Create the data directory automatically if it does not exist.
    DATA_DIRECTORY.mkdir(exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)

    # Rows can later be accessed like dictionaries:
    # row["name"] instead of row[1].
    connection.row_factory = sqlite3.Row

    return connection


def initialize_database() -> None:
    """Create the database tables when they do not already exist."""

    connection = get_database_connection()

    try:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS devices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                device_type TEXT NOT NULL,
                manufacturer TEXT,
                model TEXT,
                serial_number TEXT NOT NULL UNIQUE,
                location TEXT,
                status TEXT NOT NULL
            )
            """
        )

        connection.commit()
    finally:
        connection.close()
