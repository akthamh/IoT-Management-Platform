import sqlite3

from modules.database import get_database_connection


def create_tenant(name: str, address: str | None) -> int:
    """Save one tenant in SQLite and return its generated ID."""

    connection = get_database_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO tenants (
                name,
                address
            )
            VALUES (?, ?)
            """,
            (
                name,
                address,
            ),
        )

        connection.commit()
        return int(cursor.lastrowid)
    finally:
        connection.close()


def get_all_tenants() -> list[sqlite3.Row]:
    """Read and return all tenants from SQLite."""

    connection = get_database_connection()

    try:
        cursor = connection.execute(
            """
            SELECT
                id,
                name,
                address,
                is_active,
                created_at
            FROM tenants
            ORDER BY id
            """
        )

        return cursor.fetchall()
    finally:
        connection.close()


def get_tenant_by_id(tenant_id: int) -> sqlite3.Row | None:
    """Return one tenant by ID, or None when it does not exist."""

    connection = get_database_connection()

    try:
        cursor = connection.execute(
            """
            SELECT
                id,
                name,
                address,
                is_active,
                created_at
            FROM tenants
            WHERE id = ?
            """,
            (tenant_id,),
        )

        return cursor.fetchone()
    finally:
        connection.close()


def search_tenants(search_text: str) -> list[sqlite3.Row]:
    """Search for tenants by name or address."""

    connection = get_database_connection()

    try:
        search_pattern = f"%{search_text}%"

        cursor = connection.execute(
            """
            SELECT
                id,
                name,
                address,
                is_active,
                created_at
            FROM tenants
            WHERE name LIKE ? OR address LIKE ?
            ORDER BY id
            """,
            (
                search_pattern,
                search_pattern,
            ),
        )

        return cursor.fetchall()
    finally:
        connection.close()