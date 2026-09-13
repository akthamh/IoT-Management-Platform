# Multi-Tenant IoT Management Platform

## v0.3.0 - Multi-Tenant Foundation

This educational release introduces tenant management and links IoT devices to tenants while keeping the project focused on Python, SQLite, modules, and a command-line interface.

The platform now supports multiple tenants, and each device can be assigned to a registered tenant.

No web frontend, React, FastAPI, Docker, MQTT, or automated device connectivity is used in this release.

## Learning goals

- Python modules and imports
- SQLite databases with Python's built-in `sqlite3` module
- SQL `INSERT`, `SELECT`, `UPDATE`, and `DELETE`
- SQL `JOIN`
- SQL foreign keys
- database schema migration
- parameterized SQL queries
- primary keys and foreign keys
- input validation
- reusable Python functions
- separation between CLI logic and database access
- basic multi-tenant data relationships

## Features

### Tenant management

- register tenants
- list registered tenants
- find a tenant by ID
- search tenants by name or address
- store tenant data permanently in SQLite
- automatically store tenant creation time
- track whether a tenant is active

### Device management

- selectable IoT device catalog
- manual device registration
- persistent SQLite storage
- list all registered devices
- search by device name or serial number
- update an existing device by ID
- delete a device by ID with explicit confirmation
- reject duplicate serial numbers

### Multi-Tenant Device Management

- assign devices to registered tenants
- store the tenant relationship using `tenant_id`
- use a foreign key between devices and tenants
- display the tenant name with device information
- search devices together with tenant information
- change a device's tenant during an update
- preserve existing device data during the database migration

## Development progress

- [x] Create SQLite database connection
- [x] Create the `devices` table
- [x] Create the `tenants` table
- [x] Create tenant repository
- [x] Create tenant manager
- [x] Register tenants
- [x] List tenants
- [x] Find tenant by ID
- [x] Search tenants
- [x] Add `tenant_id` to existing devices
- [x] Add foreign-key relationship between devices and tenants
- [x] Assign existing devices to tenants
- [x] Select a tenant when registering a device
- [x] Display tenant names with devices
- [x] Search devices with tenant information
- [x] Change a device's tenant during update
- [x] Preserve existing SQLite device persistence
- [x] Complete manual testing

## Project structure

```text
iot-management-platform/
|
|-- main.py
|
|-- modules/
|   |-- __init__.py
|   |-- database.py
|   |-- device_catalog.py
|   |-- device_manager.py
|   |-- device_repository.py
|   |-- tenant_manager.py
|   `-- tenant_repository.py
|
|-- data/
|   `-- iot_platform.db
|
|-- docs/
|   `-- releases/
|       |-- v0.1.0.md
|       |-- v0.2.0.md
|       `-- v0.3.0.md
|
|-- .gitignore
`-- README.md
```

The `data` directory and database file are created automatically.

Runtime database files are ignored by Git because they contain local application data.

## Run the project

Open PowerShell in the project directory and run:

```powershell
python main.py
```

The CLI provides tenant-management and device-management operations.

## Application data flow

Tenant operations:

```text
User
 |
 v
main.py
 |
 v
tenant_manager.py
 |
 v
tenant_repository.py
 |
 v
database.py
 |
 v
SQLite
```

Device operations:

```text
User
 |
 v
main.py
 |
 v
device_manager.py
 |
 v
device_repository.py
 |
 v
database.py
 |
 v
SQLite
```

## Module responsibilities

### `main.py`

- initializes the database
- displays the main application menu
- routes the user to tenant or device operations

### `modules/database.py`

- creates the local data directory
- opens SQLite connections
- enables foreign-key support
- creates the `tenants` table
- creates the `devices` table
- migrates an existing device table when `tenant_id` is missing

### `modules/device_catalog.py`

- stores supported IoT categories and device types
- lets the user select a supported device type

### `modules/device_repository.py`

- contains parameterized SQL queries for devices
- creates, reads, searches, updates, and deletes device records
- stores `tenant_id`
- joins the `devices` and `tenants` tables
- returns tenant information together with device information

### `modules/device_manager.py`

- reads and validates device-related user input
- lets the user select a tenant when adding a device
- displays the tenant name with device information
- controls add, list, search, update, and delete workflows
- allows changing the assigned tenant during a device update
- asks for confirmation before saving changes or deleting data

### `modules/tenant_repository.py`

- contains SQLite operations for tenants
- creates tenant records
- lists tenants
- finds a tenant by ID
- searches tenants by name or address
- keeps SQL separate from the CLI

### `modules/tenant_manager.py`

- collects and validates tenant input
- displays tenant information
- controls tenant-management workflows

## SQLite tenant table

Each tenant contains:

- generated numeric ID
- name
- optional address
- active/inactive value
- automatic creation timestamp

Schema:

```text
tenants
----------------------------------------------------------
id           INTEGER PRIMARY KEY AUTOINCREMENT
name         TEXT NOT NULL
address      TEXT
is_active    INTEGER NOT NULL DEFAULT 1
created_at   TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
```

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
- tenant ID

Relationship:

```text
tenants.id
    |
    v
devices.tenant_id
```

`tenant_id` is used internally to connect a device to its tenant.

The CLI displays the tenant name instead of requiring the user to work directly with the tenant ID.

## Multi-Tenant relationship

The platform separates tenant information from device information.

Example:

```text
Test Tenant
|
|-- Rum01_Temp01
`-- front_cam01

ERaqaeq AB
|
`-- Cont_LKP_RYD_158
```

SQLite stores the relationship using:

```text
devices.tenant_id -> tenants.id
```

Device queries use SQL `JOIN` operations to retrieve the tenant name together with device information.

## Database migration

`v0.2.0` devices existed before tenant support was introduced.

During development of `v0.3.0`, the existing `devices` table was extended with:

```text
tenant_id INTEGER
```

The migrated `tenant_id` column remains nullable at the database level for compatibility with existing records.

The CLI requires a tenant when registering new devices.

Existing device records were preserved and assigned to tenants.

The migration avoids deleting the existing SQLite database and demonstrates how an application can evolve its database structure while preserving stored data.

## Previous releases

### v0.2.0 - SQLite Device Persistence

Introduced persistent SQLite device storage, CRUD operations, search, validation, and duplicate serial-number handling.

### v0.1.0 - Python CLI Foundation

Introduced the Python CLI, modules, device catalog, and temporary in-memory device registration.

See:

- `docs/releases/v0.1.0.md`
- `docs/releases/v0.2.0.md`
- `docs/releases/v0.3.0.md`
