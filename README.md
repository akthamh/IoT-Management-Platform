# Multi-Tenant IoT Management Platform

## v0.4.0 - Object-Oriented Multi-Tenant Core (In Development)

This educational development version extends the multi-tenant foundation from `v0.3.0` by introducing object-oriented programming for the core platform entities while keeping the project focused on Python, SQLite, modules, and a command-line interface.

The platform still supports multiple tenants, and each device can be assigned to a registered tenant.

`Tenant` and `Device` are now represented as Python classes and objects instead of passing raw `sqlite3.Row` values or dictionaries through the application.

No web frontend, React, FastAPI, Docker, MQTT, or automated device connectivity is used in this release.

## Learning goals

- Python classes and objects
- `__init__` and `self`
- object attributes
- type hints
- converting SQLite rows into Python objects
- separation between database rows and application objects
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
- represent tenants as `Tenant` objects

### Device management

- selectable IoT device catalog
- manual device registration
- persistent SQLite storage
- list all registered devices
- search by device name or serial number
- update an existing device by ID
- delete a device by ID with explicit confirmation
- reject duplicate serial numbers
- represent devices as `Device` objects

### Multi-Tenant Device Management

- assign devices to registered tenants
- store the tenant relationship using `tenant_id`
- use a foreign key between devices and tenants
- display the tenant name with device information
- search devices together with tenant information
- change a device's tenant during an update
- preserve existing device data during the database migration

### Object-Oriented Core

The main platform entities are now represented by classes:

- `Tenant`
- `Device`

Application code now works with object attributes such as:

```python
tenant.id
tenant.name

device.id
device.name
device.status
device.tenant_id
```

instead of dictionary-style access such as:

```python
tenant["name"]
device["name"]
```

Repository functions convert SQLite rows into model objects before returning data to the rest of the application.

## Development progress

### Multi-tenant foundation completed in v0.3.0

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

### Object-oriented foundation completed in v0.4.0 development

- [x] Add `Tenant` model class
- [x] Add `Device` model class
- [x] Add type hints to model attributes
- [x] Convert tenant repository reads to return `Tenant` objects
- [x] Convert `create_tenant()` to return a `Tenant` object
- [x] Update tenant manager code to use object attributes
- [x] Convert device repository reads to return `Device` objects
- [x] Convert `create_device()` to accept and return a `Device` object
- [x] Convert `update_device()` to accept a `Device` object
- [x] Update device manager code to create and use `Device` objects
- [x] Update device display logic to use object attributes
- [x] Remove the old `Mapping`-based device representation from the device lifecycle
- [x] Verify create, list, get, search, and update operations after the OOP migration


## Project structure

```text
iot-management-platform/
│
├── main.py
│
├── modules/
│   ├── __init__.py
│   ├── database.py
│   ├── device_catalog.py
│   ├── device_manager.py
│   ├── device_repository.py
│   ├── tenant_manager.py
│   └── tenant_repository.py
|   └── models/
|       ├── __init__.py
|       ├── device.py
|       └── tenant.py
|
│├── data/
│   └── iot_platform.db
│
├── docs/
│   └── releases/
│       ├── v0.1.0.md
│       ├── v0.2.0.md
│       ├── v0.3.0.md
│       └── v0.4.0.md
│
├── .gitignore
└── README.md
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
  ↓
main.py
  ↓
tenant_manager.py
  ↓
tenant_repository.py
  ↓
SQLite
  ↓
Tenant object
```

Device operations:

```text
User
  ↓
main.py
  ↓
device_manager.py
  ↓
Device object
  ↓
device_repository.py
  ↓
SQLite
```

When data is read from SQLite, repository functions convert database rows into application objects:

```text
SQLite
  ↓
sqlite3.Row
   |
   +----> Tenant(...)
   |        ↓
   |      Tenant object
   |
   `----> Device(...)
            ↓
          Device object
```

## Model responsibilities

### `modules/models/tenant.py`

Represents one tenant in the application.

Current attributes:

```text
id
name
address
is_active
created_at
```

The tenant ID can be `None` before a new tenant is stored in SQLite.

`is_active` is represented as a Python `bool`, while SQLite stores it as an integer.

### `modules/models/device.py`

Represents one IoT device in the application.

Current attributes:

```text
id
name
category
device_type
manufacturer
model
serial_number
location
status
tenant_id
```

The device ID can be `None` while a new `Device` object exists only in memory and has not yet been saved.

The device stores `tenant_id` rather than duplicating the tenant name inside the `Device` model.

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
- converts SQLite rows into `Device` objects
- accepts `Device` objects for create and update operations

### `modules/device_manager.py`

- reads and validates device-related user input
- creates `Device` objects from validated user input
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
- converts SQLite rows into `Tenant` objects
- returns `Tenant` objects instead of raw database rows

### `modules/tenant_manager.py`

- collects and validates tenant input
- displays `Tenant` objects
- coordinates tenant-management operations between user input and the repository
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
    ↓
devices.tenant_id
```

`tenant_id` is used internally to connect a device to its tenant.

The CLI displays the tenant name instead of requiring the user to work directly with the tenant ID.

Inside Python, a `Device` object keeps the relationship through:

```python
device.tenant_id
```

The corresponding tenant can then be retrieved as a `Tenant` object when its information is needed.

## Multi-Tenant relationship

The platform separates tenant information from device information.

Example:

```text
Test Tenant
    │
    ├── Rum01_Temp01
    └── front_cam01

ERaqaeq AB
    │
    └── Cont_LKP_RYD_158
```

SQLite stores the relationship using:

```text
devices.tenant_id → tenants.id
```

The object-oriented application layer preserves the same relationship:

```text
Device object
    ↓
 tenant_id
    ↓
Tenant object
```

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

The OOP work in `v0.4.0` changes the Python application layer and does not require a new database schema for the completed OOP foundation.

## Why OOP in v0.4.0?

Earlier releases used dictionaries and `sqlite3.Row` values directly in several parts of the application.

That approach was useful while building the Python and SQLite foundation.

The project now has stable core entities with clear identities:

```text
Tenant
Device
```

Using classes gives these entities a consistent application representation and prepares the platform for future development.

Not every module is converted into a class. Simple helpers, menu logic, and database connection functions remain functions where a class would not add useful state or behavior.

## Previous releases

### v0.3.0 — Multi-Tenant Foundation

Introduced tenant management, the `tenant_id` relationship, SQLite foreign keys, tenant-aware device registration, and multi-tenant database structure.

### v0.2.0 — SQLite Device Persistence

Introduced persistent SQLite device storage, CRUD operations, search, validation, and duplicate serial-number handling.

### v0.1.0 — Python CLI Foundation

Introduced the Python CLI, modules, device catalog, and temporary in-memory device registration.

See:

- `docs/releases/v0.1.0.md`
- `docs/releases/v0.2.0.md`
- `docs/releases/v0.3.0.md`