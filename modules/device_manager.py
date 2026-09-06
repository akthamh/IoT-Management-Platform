import sqlite3
from collections.abc import Mapping

from modules.device_catalog import choose_device_type
from modules.device_repository import (
    create_device,
    get_all_devices,
    search_devices,
)


def ask_required_text(message: str) -> str:
    """Ask for text and reject empty input."""

    while True:
        value = input(message).strip()

        if value:
            return value

        print("This field cannot be empty.")


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
    device: Mapping[str, str | int | None],
) -> None:
    """Print one device in a consistent readable format."""

    # A new device has no ID until SQLite saves it.
    device_id = device["id"] if "id" in device else "Generated when saved"

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

    search_text = input(
        "\nEnter device name or serial number: "
    ).strip()

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