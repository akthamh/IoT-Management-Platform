import sqlite3
from collections.abc import Mapping

from modules.database import get_database_connection


def create_device(device: Mapping[str, str]) -> int:
    """Save one device in SQLite and return its generated ID."""

    connection = get_database_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO devices (
                name,
                category,
                device_type,
                manufacturer,
                model,
                serial_number,
                location,
                status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                device["name"],
                device["category"],
                device["device_type"],
                device["manufacturer"],
                device["model"],
                device["serial_number"],
                device["location"],
                device["status"],
            ),
        )

        connection.commit()
        return int(cursor.lastrowid)
    finally:
        connection.close()


def get_all_devices() -> list[sqlite3.Row]:
    """Read and return all devices from SQLite."""

    connection = get_database_connection()

    try:
        cursor = connection.execute(
            """
            SELECT
                id,
                name,
                category,
                device_type,
                manufacturer,
                model,
                serial_number,
                location,
                status
            FROM devices
            ORDER BY id
            """
        )

        return cursor.fetchall()
    finally:
        connection.close()


def get_device_by_id(device_id: int) -> sqlite3.Row | None:
    """Return one device by ID, or None when it does not exist."""

    connection = get_database_connection()

    try:
        cursor = connection.execute(
            """
            SELECT
                id,
                name,
                category,
                device_type,
                manufacturer,
                model,
                serial_number,
                location,
                status
            FROM devices
            WHERE id = ?
            """,
            (device_id,),
        )

        return cursor.fetchone()
    finally:
        connection.close()


def search_devices(search_text: str) -> list[sqlite3.Row]:
    """Search for devices by name or serial number."""

    connection = get_database_connection()

    try:
        search_pattern = f"%{search_text}%"

        cursor = connection.execute(
            """
            SELECT
                id,
                name,
                category,
                device_type,
                manufacturer,
                model,
                serial_number,
                location,
                status
            FROM devices
            WHERE name LIKE ? OR serial_number LIKE ?
            ORDER BY id
            """,
            (search_pattern, search_pattern),
        )

        return cursor.fetchall()
    finally:
        connection.close()


def update_device(device_id: int, device: Mapping[str, str]) -> bool:
    """Update one device and return True when the device exists."""

    connection = get_database_connection()

    try:
        cursor = connection.execute(
            """
            UPDATE devices
            SET
                name = ?,
                category = ?,
                device_type = ?,
                manufacturer = ?,
                model = ?,
                serial_number = ?,
                location = ?,
                status = ?
            WHERE id = ?
            """,
            (
                device["name"],
                device["category"],
                device["device_type"],
                device["manufacturer"],
                device["model"],
                device["serial_number"],
                device["location"],
                device["status"],
                device_id,
            ),
        )

        connection.commit()
        return cursor.rowcount > 0
    finally:
        connection.close()


def delete_device(device_id: int) -> bool:
    """Delete one device and return True when the device exists."""

    connection = get_database_connection()

    try:
        cursor = connection.execute(
            "DELETE FROM devices WHERE id = ?",
            (device_id,),
        )

        connection.commit()
        return cursor.rowcount > 0
    finally:
        connection.close()
