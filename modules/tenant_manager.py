import sqlite3
from collections.abc import Mapping

from modules.tenant_repository import (
    create_tenant,
    get_all_tenants,
    get_tenant_by_id,
    search_tenants,
)


def ask_required_text(message: str) -> str:
    """Ask for text and reject empty input."""

    while True:
        value = input(message).strip()

        if value:
            return value

        print("This field cannot be empty.")


def ask_tenant_id() -> int | None:
    """Ask for a positive tenant ID, or return None when cancelled."""

    while True:
        value = input("\nEnter tenant ID (0 to cancel): ").strip()

        if value == "0":
            return None

        if value.isdigit() and int(value) > 0:
            return int(value)

        print("Please enter a positive tenant ID or 0 to cancel.")


def add_tenant() -> None:
    """Collect tenant information and save it in SQLite."""

    print("\n" + "=" * 40)
    print("              Add Tenant")
    print("=" * 40)

    name = ask_required_text("\nTenant name: ")
    address = input("Address (optional): ").strip()

    print("\nReview tenant")
    print("-" * 30)
    print(f"Name:    {name}")
    print(f"Address: {address or '-'}")

    confirm = input("\nSave this tenant? (y/n): ").strip().lower()

    if confirm != "y":
        print("\nTenant was not saved.")
        return

    tenant_id = create_tenant(
        name,
        address or None,
    )

    print(f"\nTenant added successfully with ID {tenant_id}.")


def print_tenant(
    tenant: Mapping[str, object] | sqlite3.Row,
) -> None:
    """Print one tenant in a consistent readable format."""

    print(f"ID:         {tenant['id']}")
    print(f"Name:       {tenant['name']}")
    print(f"Address:    {tenant['address'] or '-'}")

    if tenant["is_active"]:
        status = "Active"
    else:
        status = "Inactive"

    print(f"Status:     {status}")
    print(f"Created at: {tenant['created_at']}")


def list_tenants() -> None:
    """Read and display all tenants stored in SQLite."""

    print("\n" + "=" * 40)
    print("          Registered Tenants")
    print("=" * 40)

    tenants = get_all_tenants()

    if not tenants:
        print("\nNo tenants have been registered yet.")
        return

    for tenant in tenants:
        print()
        print_tenant(tenant)
        print("-" * 30)


def find_tenant() -> None:
    """Find and display one tenant by ID."""

    tenant_id = ask_tenant_id()

    if tenant_id is None:
        print("\nSearch cancelled.")
        return

    tenant = get_tenant_by_id(tenant_id)

    if tenant is None:
        print("\nTenant not found.")
        return

    print("\nTenant details")
    print("-" * 30)
    print_tenant(tenant)


def search_tenant() -> None:
    """Search SQLite for tenants by name or address."""

    search_text = input(
        "\nEnter tenant name or address: "
    ).strip()

    if not search_text:
        print("Search text cannot be empty.")
        return

    results = search_tenants(search_text)

    if not results:
        print("\nNo matching tenants found.")
        return

    print(f"\nFound {len(results)} matching tenant(s):")

    for tenant in results:
        print()
        print_tenant(tenant)
        print("-" * 30)
