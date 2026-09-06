# Multi-Tenant IoT Management Platform

## v0.1.0 — Python CLI + Modules + Manual Device Registration

This is the first educational version of the IoT Management Platform.

The goal of this version is to practice core Python concepts from the course while building a real project step by step.

## Learning goals

This version uses:

- Python
- functions
- modules
- imports
- lists
- dictionaries
- loops
- conditions
- user input
- basic validation

No web frontend, React, FastAPI, Docker, or MQTT is used in this version.

## Features

- Main menu
- Device catalog
- Device categories
- Select a device type from the catalog
- Manually register a device
- List registered devices
- Search registered devices by name or serial number
- Data is stored in memory while the program is running

> Important: Device data is not persistent yet. When the program closes, the current device list is lost. SQLite database persistence will be added in the next version.

---

## Project structure

```text
iot-management-platform/
│
├── main.py
├── modules/
│   ├── __init__.py
│   ├── device_catalog.py
│   └── device_manager.py
│
├── docs/
│   └── releases/
│       └── v0.1.0.md
│
├── .gitignore
└── README.md
```

---

## Run the project

Open PowerShell in the project folder and run:

```powershell
python main.py
```

Expected menu:

```text
========================================
       IoT Management Platform
========================================

1. Add new device
2. List devices
3. Search device
4. Show device catalog
0. Exit
```

---

## Device registration flow

When adding a device:

```text
Add Device
   ↓
Choose Category
   ↓
Choose Device Type
   ↓
Enter Device Information
   ↓
Review
   ↓
Save in memory
```

Example:

```text
Category: Sensors
Device type: Temperature Sensor

Device name: Server Room Sensor
Manufacturer: Bosch
Model: ABC123
Serial number: TEMP-001
Location: Server Room
Status: Active
```

---

## Why use modules?

Instead of writing everything inside `main.py`, the project is divided into smaller modules.

### `main.py`

Responsible for:

- showing the main menu
- reading the user's menu choice
- calling functions from other modules

### `modules/device_catalog.py`

Responsible for:

- storing supported device categories
- storing supported device types
- showing categories
- letting the user choose a device type

### `modules/device_manager.py`

Responsible for:

- adding devices
- listing devices
- searching devices

This makes the code easier to read, test, maintain, and expand.

---

## Git workflow for v0.1.0

If this is a new repository:

```powershell
git init
```

Check the current status:

```powershell
git status
```

Create the feature branch:

```powershell
git switch -c feature/python-cli-foundation
```

Run and test the program:

```powershell
python main.py
```

Then check changes:

```powershell
git status
git diff
```

Stage files:

```powershell
git add .
```

Review what will be committed:

```powershell
git diff --cached
```

Commit:

```powershell
git commit -m "Build v0.1.0 Python CLI foundation"
```

If the GitHub remote already exists:

```powershell
git push -u origin feature/python-cli-foundation
```

Suggested Pull Request title:

```text
Build v0.1.0 Python CLI foundation
```

Suggested PR summary:

```text
## Summary
Creates the first educational version of the IoT Management Platform.

## Included
- Python CLI menu
- modular project structure
- device catalog
- manual device registration
- device listing
- device search

## Learning focus
- functions
- modules
- lists
- dictionaries
- loops
- conditions
- input validation
```

After merge:

```powershell
git switch main
git pull
```

Then tag the version:

```powershell
git tag -a v0.1.0 -m "Python CLI and modules foundation"
git push origin v0.1.0
```

---

## Definition of Done

v0.1.0 is complete when:

- [ ] `python main.py` starts successfully
- [ ] Main menu works
- [ ] Device catalog can be displayed
- [ ] User can choose a device category
- [ ] User can choose a device type
- [ ] User can manually add a device
- [ ] User can list devices
- [ ] User can search devices
- [ ] Invalid menu choices are handled
- [ ] README is updated
- [ ] Git commit is created
- [ ] Pull Request is merged
- [ ] Git tag `v0.1.0` is created

---

## Next version

### v0.2.0 — SQLite Database

The next version will replace temporary in-memory storage with a real SQLite database using Python's built-in `sqlite3` module.

That version will introduce:

- database connection
- device table
- save devices permanently
- read devices from SQLite
- update device
- delete device
