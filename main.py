from modules.database import initialize_database
from modules.device_catalog import show_full_catalog
from modules.device_manager import (
    add_device,
    delete_device,
    list_devices,
    search_device,
    update_device,
)


def show_main_menu() -> None:
    """Display the main application menu."""

    print("\n" + "=" * 40)
    print("       IoT Management Platform")
    print("=" * 40)
    print("1. Add new device")
    print("2. List devices")
    print("3. Search device")
    print("4. Show device catalog")
    print("5. Update device")
    print("6. Delete device")
    print("0. Exit")


def main() -> None:
    """Initialize the database and run the main program loop."""

    initialize_database()

    while True:
        show_main_menu()
        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            add_device()
        elif choice == "2":
            list_devices()
        elif choice == "3":
            search_device()
        elif choice == "4":
            show_full_catalog()
        elif choice == "5":
            update_device()
        elif choice == "6":
            delete_device()
        elif choice == "0":
            print("\nGoodbye!")
            break
        else:
            print("\nInvalid choice. Please choose one of the menu options.")


if __name__ == "__main__":
    main()
