# Multi-Tenant IoT Management Platform

## v0.2.0 — SQLite Device Persistence

This educational release replaces temporary in-memory device storage with a persistent SQLite database while keeping the application intentionally simple and focused on Python.

## Learning goals

- Python modules and imports
- SQLite databases with Python's built-in `sqlite3` module
- SQL `INSERT`, `SELECT`, `UPDATE`, and `DELETE`
- parameterized SQL queries
- primary keys and unique serial numbers
- input validation and confirmation before destructive actions
- separation between the CLI, business flow, and data-access code

No web frontend, React, FastAPI, Docker, or MQTT is used in this release.

## Features

- selectable IoT device catalog
- manual device registration
- persistent SQLite storage
- list all registered devices
- search by device name or serial number
- update an existing device by ID
- delete a device by ID with explicit confirmation
- reject duplicate serial numbers

## Development progress

- [x] Create SQLite database connection
- [x] Create the `devices` table
- [x] Save devices permanently
- [x] Read devices from SQLite
- [x] Search devices in SQLite
- [x] Reject duplicate serial numbers
- [x] Update devices
- [x] Delete devices
- [x] Complete final manual testing

## Project structure

```text
iot-management-platform/
│
├── main.py
├── modules/
│   ├── __init__.py
│   ├── database.py
│   ├── device_catalog.py
│   ├── device_manager.py
│   └── device_repository.py
│
├── data/
│   └── iot_platform.db
│
├── docs/
│   └── releases/
│       ├── v0.1.0.md
│       └── v0.2.0.md
│
├── .gitignore
└── README.md
```

The `data` directory and database file are created automatically. Runtime database files are ignored by Git because they contain local application data.

## Run the project

Open PowerShell in the project directory and run:

```powershell
python main.py
```

Expected menu:

```
========================================
       IoT Management Platform
========================================
1. Add new device
2. List devices
3. Search device
4. Show device catalog
5. Update device
6. Delete device
0. Exit
```

## Module responsibilities

### `main.py`

- initializes the database
- displays the main menu
- calls the selected device-management function

### `modules/database.py`

- creates the local data directory
- opens SQLite connections
- creates the `devices` table

### `modules/device_catalog.py`

- stores supported IoT categories and device types
- lets the user select a supported device type

### `modules/device_repository.py`

- contains parameterized SQL queries
- creates, reads, searches, updates, and deletes device records

### `modules/device_manager.py`

- reads and validates user input
- controls add, list, search, update, and delete workflows
- asks for confirmation before saving changes or deleting data

## SQLite device table

Each device contains:

- generated numeric ID
- name
- category
- device type
- manufacturer
- model
- unique serial number
- location
- status

## Previous release

`v0.1.0` introduced the Python CLI, modules, device catalog, and temporary in-memory device registration.

See [`docs/releases/v0.1.0.md`](docs/releases/v0.1.0.md) and [`docs/releases/v0.2.0.md`](docs/releases/v0.2.0.md) for release-specific details.
