import sqlite3
from collections.abc import Mapping

from modules.device_catalog import choose_device_type
from modules.device_repository import (
    create_device,
    delete_device as delete_device_from_database,
    get_all_devices,
    get_device_by_id,
    search_devices,
    update_device as update_device_in_database,
)


def ask_required_text(message: str) -> str:
    """Ask for text and reject empty input."""

    while True:
        value = input(message).strip()

        if value:
            return value

        print("This field cannot be empty.")


def ask_device_id(action: str) -> int | None:
    """Ask for a positive device ID, or return None when cancelled."""

    while True:
        value = input(f"\nEnter the device ID to {action} (0 to cancel): ").strip()

        if value == "0":
            return None

        if value.isdigit() and int(value) > 0:
            return int(value)

        print("Please enter a positive device ID or 0 to cancel.")


def choose_status() -> str:
    """Let the user choose a device status from a controlled list."""

    statuses = [
        "Active",
        "Inactive",
        "Maintenance",
        "Offline",
    ]

    while True:
        print("\nDevice status")

        for index, status in enumerate(statuses, start=1):
            print(f"{index}. {status}")

        choice = input("Choose status: ").strip()

        if not choice.isdigit():
            print("Please enter a number.")
            continue

        status_index = int(choice) - 1

        if 0 <= status_index < len(statuses):
            return statuses[status_index]

        print("Invalid status.")


def add_device() -> None:
    """Collect device information and save it in SQLite."""

    print("\n" + "=" * 40)
    print("             Add Device")
    print("=" * 40)

    selection = choose_device_type()

    if selection is None:
        print("\nDevice registration cancelled.")
        return

    category, device_type = selection

    print(f"\nSelected category: {category}")
    print(f"Selected type:     {device_type}")

    device = {
        "name": ask_required_text("\nDevice name: "),
        "category": category,
        "device_type": device_type,
        "manufacturer": input("Manufacturer (optional): ").strip(),
        "model": input("Model (optional): ").strip(),
        # Normalizing the serial number prevents case differences
        # such as temp-001 and TEMP-001.
        "serial_number": ask_required_text("Serial number: ").upper(),
        "location": input("Location (optional): ").strip(),
        "status": choose_status(),
    }

    print("\nReview device")
    print("-" * 30)
    print_device(device)

    confirm = input("\nSave this device? (y/n): ").strip().lower()

    if confirm != "y":
        print("\nDevice was not saved.")
        return

    try:
        device_id = create_device(device)
    except sqlite3.IntegrityError:
        print("\nA device with this serial number already exists.")
        return

    print(f"\nDevice added successfully with ID {device_id}.")


def print_device(
    device: Mapping[str, str | int | None] | sqlite3.Row,
) -> None:
    """Print one device in a consistent readable format."""

    # New unsaved dictionaries have no ID, while SQLite rows always do.
    try:
        device_id = device["id"]
    except (KeyError, IndexError):
        device_id = "Generated when saved"

    print(f"ID:           {device_id}")
    print(f"Name:         {device['name']}")
    print(f"Category:     {device['category']}")
    print(f"Type:         {device['device_type']}")
    print(f"Manufacturer: {device['manufacturer'] or '-'}")
    print(f"Model:        {device['model'] or '-'}")
    print(f"Serial:       {device['serial_number']}")
    print(f"Location:     {device['location'] or '-'}")
    print(f"Status:       {device['status']}")


def list_devices() -> None:
    """Read and display all devices stored in SQLite."""

    print("\n" + "=" * 40)
    print("          Registered Devices")
    print("=" * 40)

    devices = get_all_devices()

    if not devices:
        print("\nNo devices have been registered yet.")
        return

    for device in devices:
        print()
        print_device(device)
        print("-" * 30)


def search_device() -> None:
    """Search SQLite for devices by name or serial number."""

    search_text = input("\nEnter device name or serial number: ").strip()

    if not search_text:
        print("Search text cannot be empty.")
        return

    results = search_devices(search_text)

    if not results:
        print("\nNo matching devices found.")
        return

    print(f"\nFound {len(results)} matching device(s):")

    for device in results:
        print()
        print_device(device)
        print("-" * 30)


def update_device() -> None:
    """Let the user update an existing device."""

    print("\n" + "=" * 40)
    print("            Update Device")
    print("=" * 40)

    device_id = ask_device_id("update")

    if device_id is None:
        print("\nUpdate cancelled.")
        return

    current_device = get_device_by_id(device_id)

    if current_device is None:
        print("\nDevice not found.")
        return

    print("\nCurrent device")
    print("-" * 30)
    print_device(current_device)

    category = str(current_device["category"])
    device_type = str(current_device["device_type"])

    change_type = input("\nChange category and device type? (y/n): ").strip().lower()

    if change_type == "y":
        selection = choose_device_type()

        if selection is not None:
            category, device_type = selection

    current_name = str(current_device["name"])
    current_serial = str(current_device["serial_number"])

    updated_device = {
        "name": input(f"Name [{current_name}]: ").strip() or current_name,
        "category": category,
        "device_type": device_type,
        "manufacturer": ask_optional_update(
            "Manufacturer",
            current_device["manufacturer"],
        ),
        "model": ask_optional_update("Model", current_device["model"]),
        "serial_number": (
            input(f"Serial number [{current_serial}]: ").strip() or current_serial
        ).upper(),
        "location": ask_optional_update("Location", current_device["location"]),
        "status": str(current_device["status"]),
    }

    change_status = input("Change status? (y/n): ").strip().lower()

    if change_status == "y":
        updated_device["status"] = choose_status()

    print("\nReview updated device")
    print("-" * 30)
    print_device({"id": device_id, **updated_device})

    confirm = input("\nSave these changes? (y/n): ").strip().lower()

    if confirm != "y":
        print("\nChanges were not saved.")
        return

    try:
        updated = update_device_in_database(device_id, updated_device)
    except sqlite3.IntegrityError:
        print("\nA device with this serial number already exists.")
        return

    if updated:
        print("\nDevice updated successfully.")
    else:
        print("\nDevice not found.")


def ask_optional_update(label: str, current_value: object) -> str:
    """Keep, replace, or clear an optional text field."""

    current_text = "" if current_value is None else str(current_value)
    display_value = current_text or "-"
    value = input(f"{label} [{display_value}] (Enter to keep, - to clear): ").strip()

    if not value:
        return current_text

    if value == "-":
        return ""

    return value


def delete_device() -> None:
    """Delete a device only after explicit confirmation."""

    print("\n" + "=" * 40)
    print("            Delete Device")
    print("=" * 40)

    device_id = ask_device_id("delete")

    if device_id is None:
        print("\nDeletion cancelled.")
        return

    device = get_device_by_id(device_id)

    if device is None:
        print("\nDevice not found.")
        return

    print("\nDevice to delete")
    print("-" * 30)
    print_device(device)

    confirm = input("\nType DELETE to confirm: ").strip()

    if confirm != "DELETE":
        print("\nDeletion cancelled.")
        return

    if delete_device_from_database(device_id):
        print("\nDevice deleted successfully.")
    else:
        print("\nDevice not found.")
