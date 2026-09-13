from modules.database import initialize_database
from modules.device_catalog import show_full_catalog
from modules.device_manager import (
    add_device,
    delete_device,
    list_devices,
    search_device,
    update_device,
)

from modules.tenant_manager import (
    add_tenant,
    find_tenant,
    list_tenants,
    search_tenant,
)

def show_main_menu() -> None:
    """Display the main application menu."""

    print("\n" + "=" * 40)
    print("       IoT Management Platform")
    print("=" * 40)

    print("\nTenant Management")
    print("1. Add tenant")
    print("2. List tenants")
    print("3. Find tenant by ID")
    print("4. Search tenant")

    print("\nDevice Management")
    print("5. Add new device")
    print("6. List devices")
    print("7. Search device")
    print("8. Show device catalog")
    print("9. Update device")
    print("10. Delete device")

    print("\n0. Exit")


def main() -> None:
    """Initialize the database and run the main program loop."""

    initialize_database()

    while True:
        show_main_menu()
        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            add_tenant()
        elif choice == "2":
            list_tenants()
        elif choice == "3":
            find_tenant()
        elif choice == "4":
            search_tenant()
        elif choice == "5":
            add_device()
        elif choice == "6":
            list_devices()
        elif choice == "7":
            search_device()
        elif choice == "8":
            show_full_catalog()
        elif choice == "9":
            update_device()
        elif choice == "10":
            delete_device()
        elif choice == "0":
            print("\nGoodbye!")
            break
        else:
            print("\nInvalid choice. Please choose one of the menu options.")


if __name__ == "__main__":
    main()
