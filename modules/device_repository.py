import sqlite3

from modules.database import get_database_connection
from modules.models.device import Device

def create_device(device: Device) -> Device:
    """Save one device in SQLite and return it as Device object."""

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
                status,
                tenant_id
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                device.name,
                device.category,
                device.device_type,
                device.manufacturer,
                device.model,
                device.serial_number,
                device.location,
                device.status,
                device.tenant_id,
            ),
        )

        connection.commit()
        device_id = int(cursor.lastrowid)
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
                status,
                tenant_id
            FROM devices
            WHERE id = ?
            """,
            (device_id,),
        )

        row = cursor.fetchone()
        if row is None:
            raise RuntimeError("Failed to read the newly created device.")
        return Device(
            id=row["id"],
            name=row["name"],
            category=row["category"],
            device_type=row["device_type"],
            manufacturer=row["manufacturer"],
            model=row["model"],
            serial_number=row["serial_number"],
            location=row["location"],
            status=row["status"],
            tenant_id=row["tenant_id"],
        )
    finally:
        connection.close()


def get_all_devices() -> list[Device]:
    """Read and return all devices as a list of objects from SQLite."""

    connection = get_database_connection()

    try:
        cursor = connection.execute(
            """
            SELECT
                devices.id,
                devices.name,
                devices.category,
                devices.device_type,
                devices.manufacturer,
                devices.model,
                devices.serial_number,
                devices.location,
                devices.status,
                devices.tenant_id,
                tenants.name AS tenant_name
            FROM devices
            JOIN tenants
                ON devices.tenant_id = tenants.id
            ORDER BY devices.id
            """
        )

        rows = cursor.fetchall()
        devices = []
        for row in rows:
            device = Device(
                id=row["id"],
                name=row["name"],
                category=row["category"],
                device_type=row["device_type"],
                manufacturer=row["manufacturer"],
                model=row["model"],
                serial_number=row["serial_number"],
                location=row["location"],
                status=row["status"],
                tenant_id=row["tenant_id"],
            )
            devices.append(device)
        return devices
    finally:
        connection.close()


def get_device_by_id(device_id: int) -> Device | None:
    """Return one device by ID, or None when it does not exist."""

    connection = get_database_connection()

    try:
        cursor = connection.execute(
            """
            SELECT
                devices.id,
                devices.name,
                devices.category,
                devices.device_type,
                devices.manufacturer,
                devices.model,
                devices.serial_number,
                devices.location,
                devices.status,
                devices.tenant_id,
                tenants.name AS tenant_name
            FROM devices
            JOIN tenants
                ON devices.tenant_id = tenants.id
            WHERE devices.id = ?
            """,
            (device_id,),
        )

        row = cursor.fetchone()

        if row is None:
            return None
        return Device(
            id=row["id"],
            name=row["name"],
            category=row["category"],
            device_type=row["device_type"],
            manufacturer=row["manufacturer"],
            model=row["model"],
            serial_number=row["serial_number"],
            location=row["location"],
            status=row["status"],
            tenant_id=row["tenant_id"],
        )

    finally:
        connection.close()


def search_devices(search_text: str) -> list[Device]:
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
                status,
                tenant_id
            FROM devices
            WHERE name LIKE ? OR serial_number LIKE ?
            ORDER BY devices.id
            """,
            (search_pattern, search_pattern),
        )

        rows = cursor.fetchall()
        devices = []
        for row in rows:
            device = Device(
                id=row["id"],
                name=row["name"],
                category=row["category"],
                device_type=row["device_type"],
                manufacturer=row["manufacturer"],
                model=row["model"],
                serial_number=row["serial_number"],
                location=row["location"],
                status=row["status"],
                tenant_id=row["tenant_id"],
            )
            devices.append(device)
        return devices
    finally:
        connection.close()


def update_device(device: Device) -> bool:
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
                status = ?,
                tenant_id = ?
            WHERE id = ?
            """,
            (
                device.name,
                device.category,
                device.device_type,
                device.manufacturer,
                device.model,
                device.serial_number,
                device.location,
                device.status,
                device.tenant_id,
                device.id,
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
