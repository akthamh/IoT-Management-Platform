from modules.device_catalog import choose_device_type


# Devices are stored in this list only while the program is running.
#
# In v0.2.0 this temporary list will be replaced by SQLite so the data remains
# available after the program closes.
devices: list[dict[str, str | int]] = []


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
    """Register a new device manually.

    The user selects the category and type from the device catalog instead of
    typing the device type manually. This prevents inconsistent device names.
    """

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

    name = ask_required_text("\nDevice name: ")
    manufacturer = input("Manufacturer (optional): ").strip()
    model = input("Model (optional): ").strip()
    serial_number = ask_required_text("Serial number: ")
    location = input("Location (optional): ").strip()
    status = choose_status()

    # ID is generated from the current list length.
    # SQLite will generate persistent IDs in the next version.
    device_id = len(devices) + 1

    device = {
        "id": device_id,
        "name": name,
        "category": category,
        "device_type": device_type,
        "manufacturer": manufacturer,
        "model": model,
        "serial_number": serial_number,
        "location": location,
        "status": status,
    }

    print("\nReview device")
    print("-" * 30)
    print_device(device)

    confirm = input("\nSave this device? (y/n): ").strip().lower()

    if confirm == "y":
        devices.append(device)
        print("\nDevice added successfully.")
    else:
        print("\nDevice was not saved.")


def print_device(device: dict[str, str | int]) -> None:
    """Print one device in a consistent readable format."""

    print(f"ID:           {device['id']}")
    print(f"Name:         {device['name']}")
    print(f"Category:     {device['category']}")
    print(f"Type:         {device['device_type']}")
    print(f"Manufacturer: {device['manufacturer'] or '-'}")
    print(f"Model:        {device['model'] or '-'}")
    print(f"Serial:       {device['serial_number']}")
    print(f"Location:     {device['location'] or '-'}")
    print(f"Status:       {device['status']}")


def list_devices() -> None:
    """Show all devices registered during the current program session."""

    print("\n" + "=" * 40)
    print("          Registered Devices")
    print("=" * 40)

    if not devices:
        print("\nNo devices have been registered yet.")
        return

    for device in devices:
        print()
        print_device(device)
        print("-" * 30)


def search_device() -> None:
    """Search devices by name or serial number."""

    if not devices:
        print("\nNo devices have been registered yet.")
        return

    search_text = input(
        "\nEnter device name or serial number: "
    ).strip().lower()

    if not search_text:
        print("Search text cannot be empty.")
        return

    results = []

    for device in devices:
        name = str(device["name"]).lower()
        serial = str(device["serial_number"]).lower()

        if search_text in name or search_text in serial:
            results.append(device)

    if not results:
        print("\nNo matching devices found.")
        return

    print(f"\nFound {len(results)} matching device(s):")

    for device in results:
        print()
        print_device(device)
        print("-" * 30)
