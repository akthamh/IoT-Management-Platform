import sqlite3

from modules.database import get_database_connection
from modules.models.tenant import Tenant

def create_tenant(name: str, address: str | None) -> Tenant:
    """Save one tenant in SQLite and return it as a Tenant object."""

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
        tenant_id = int(cursor.lastrowid)
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
        row = cursor.fetchone()
        if row is None:
            raise RuntimeError("Failed to read the newly created tenant.")
        return Tenant(
            id=row["id"],
            name=row["name"],
            address=row["address"],
            is_active=bool(row["is_active"]),
            created_at=row["created_at"],
        )
    finally:
        connection.close()


def get_all_tenants() -> list[Tenant]:
    """Read and return all tenants as a Tenant objects from SQLite."""

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

        rows = cursor.fetchall()
        tenants = []

        for row in rows:
            tenant = Tenant(
                id=row["id"],
                name=row["name"],
                address=row["address"],
                is_active=bool(row["is_active"]),
                created_at=row["created_at"],
            )
            tenants.append(tenant)
        return tenants
    finally:
        connection.close()


def get_tenant_by_id(tenant_id: int) -> Tenant | None:
    """Return one tenant as a Tenant object by ID, or None when it does not exist."""

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
        row = cursor.fetchone()

        if row is None:
            return None
        return Tenant(
            id=row["id"],
            name=row["name"],
            address=row["address"],
            is_active=bool(row["is_active"]),
            created_at=row["created_at"],
        )
    finally:
        connection.close()


def search_tenants(search_text: str) -> list[Tenant]:
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

        rows = cursor.fetchall()
        tenants = []

        for row in rows:
            tenant = Tenant(
                id=row["id"],
                name=row["name"],
                address=row["address"],
                is_active=bool(row["is_active"]),
                created_at=row["created_at"],
            )
            tenants.append(tenant)
        return tenants
    finally:
        connection.close()