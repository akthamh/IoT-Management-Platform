# The device catalog is stored in a dictionary.
#
# Dictionary key   -> device category
# Dictionary value -> list of device types in that category
#
# This is useful for practicing dictionaries, lists, loops, functions,
# and modules while also giving the IoT project a realistic device catalog.

DEVICE_CATALOG = {
    "Sensors": [
        "Temperature Sensor",
        "Humidity Sensor",
        "Temperature & Humidity Sensor",
        "Pressure Sensor",
        "Light Sensor",
        "Motion / PIR Sensor",
        "Proximity Sensor",
        "Distance Sensor",
        "Ultrasonic Sensor",
        "Air Quality Sensor",
        "CO2 Sensor",
        "Smoke Sensor",
        "Gas Sensor",
        "Water Leak Sensor",
        "Soil Moisture Sensor",
        "Vibration Sensor",
        "Sound Sensor",
        "Accelerometer",
        "Gyroscope",
        "GPS / GNSS Sensor",
        "Current Sensor",
        "Voltage Sensor",
        "Flow Sensor",
        "Level Sensor",
        "Door / Window Sensor",
        "Occupancy Sensor",
    ],
    "Actuators": [
        "Relay",
        "Smart Relay",
        "Motor",
        "Servo Motor",
        "Stepper Motor",
        "Solenoid Valve",
        "Electric Valve",
        "Pump",
        "Fan",
        "Heater",
        "LED",
        "Smart Light",
        "Buzzer",
        "Electric Lock",
        "Smart Plug",
    ],
    "Gateways": [
        "IoT Gateway",
        "LoRaWAN Gateway",
        "Zigbee Gateway",
        "Bluetooth Gateway",
        "Wi-Fi Gateway",
        "Modbus Gateway",
        "Industrial Gateway",
        "Cellular Gateway",
        "NB-IoT Gateway",
        "LTE-M Gateway",
    ],
    "Controllers": [
        "Arduino",
        "ESP32",
        "ESP8266",
        "Raspberry Pi",
        "Raspberry Pi Pico",
        "STM32 Controller",
        "PLC",
        "Industrial Controller",
        "Edge Controller",
    ],
    "Smart Building": [
        "Smart Thermostat",
        "Smart Lighting Controller",
        "Smart Door Lock",
        "Smart Meter",
        "HVAC Controller",
        "Room Controller",
        "Occupancy Sensor",
        "Smart Smoke Detector",
        "Access Control Unit",
        "Elevator Monitoring Unit",
        "Smart Water Meter",
        "Smart Electricity Meter",
    ],
    "Energy": [
        "Electricity Meter",
        "Power Meter",
        "Smart Meter",
        "Energy Monitor",
        "Solar Inverter",
        "Battery Management System",
        "EV Charger",
        "Current Transformer",
        "Voltage Monitor",
        "Power Quality Meter",
        "Solar Panel Monitor",
    ],
    "Industrial IoT": [
        "PLC",
        "Industrial Sensor",
        "Machine Controller",
        "Motor Controller",
        "Vibration Monitor",
        "Industrial Gateway",
        "Modbus Device",
        "CAN Bus Device",
        "Production Counter",
        "Machine Condition Monitor",
        "Tank Level Monitor",
        "Flow Meter",
        "Industrial Camera",
    ],
    "Security": [
        "IP Camera",
        "CCTV Camera",
        "Door Sensor",
        "Window Sensor",
        "Motion Detector",
        "Access Control Reader",
        "RFID Reader",
        "NFC Reader",
        "Alarm Panel",
        "Smart Lock",
        "Smoke Detector",
        "Glass Break Sensor",
    ],
    "Environmental": [
        "Weather Station",
        "Air Quality Monitor",
        "CO2 Monitor",
        "Temperature Monitor",
        "Humidity Monitor",
        "Rain Sensor",
        "Wind Speed Sensor",
        "Wind Direction Sensor",
        "UV Sensor",
        "Noise Monitor",
        "Water Quality Sensor",
        "Soil Sensor",
        "Flood Sensor",
    ],
    "Network Devices": [
        "Router",
        "Switch",
        "Access Point",
        "IoT Gateway",
        "LoRaWAN Gateway",
        "Cellular Router",
        "Firewall",
        "Network Sensor",
        "Edge Gateway",
    ],
}


def show_categories() -> list[str]:
    """Print all categories and return them as a list.

    Returning the list lets another function use the same ordering when the
    user selects a category number.
    """

    categories = list(DEVICE_CATALOG.keys())

    print("\nDevice categories")
    print("-" * 30)

    for index, category in enumerate(categories, start=1):
        print(f"{index}. {category}")

    print("0. Cancel")
    return categories


def choose_device_type() -> tuple[str, str] | None:
    """Let the user choose a category and then a device type.

    Returns:
        (category, device_type) if the user makes a valid choice.
        None if the user cancels.
    """

    while True:
        categories = show_categories()
        category_choice = input("\nChoose a category: ").strip()

        if category_choice == "0":
            return None

        if not category_choice.isdigit():
            print("Please enter a number.")
            continue

        category_index = int(category_choice) - 1

        if category_index < 0 or category_index >= len(categories):
            print("Invalid category.")
            continue

        selected_category = categories[category_index]
        device_types = DEVICE_CATALOG[selected_category]

        while True:
            print(f"\n{selected_category}")
            print("-" * 30)

            for index, device_type in enumerate(device_types, start=1):
                print(f"{index}. {device_type}")

            print("0. Back")

            type_choice = input("\nChoose a device type: ").strip()

            if type_choice == "0":
                break

            if not type_choice.isdigit():
                print("Please enter a number.")
                continue

            type_index = int(type_choice) - 1

            if type_index < 0 or type_index >= len(device_types):
                print("Invalid device type.")
                continue

            return selected_category, device_types[type_index]


def show_full_catalog() -> None:
    """Display the complete supported device catalog."""

    print("\n" + "=" * 40)
    print("           Device Catalog")
    print("=" * 40)

    for category, device_types in DEVICE_CATALOG.items():
        print(f"\n{category}")
        print("-" * len(category))

        for device_type in device_types:
            print(f"- {device_type}")
