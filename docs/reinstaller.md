# Reinstaller

Reinstaller is a plugin for Mod Organizer 2 that allows users to back up downloaded mod installers and run them on demand.

## Features

- Back up files from Mod Organizer's downloads folder
- Quickly install backed up files from a convenient menu
- Store multiple versions of the same mod
- Keep Mod Organizer's downloads folder clean

## Installation

Download Reinstaller from [Nexus Mods](https://www.nexusmods.com/skyrimspecialedition/mods/59292) or [GitHub](https://github.com/Kezyma/ModOrganizer-Plugins/releases/tag/reinstaller).

Extract the `reinstaller` folder from the zip file and place it in Mod Organizer's plugins folder:
- Example: `C:\Mod Organizer\plugins\reinstaller\`

Inside the folder you should find:
- A `shared` folder
- A `reinstaller` folder
- A file called `__init__.py`

Reinstaller will start the next time you run Mod Organizer.

Alternatively, install through [Plugin Finder](pluginfinder.md) or use the [Mod Organizer Setup Tool](https://www.nexusmods.com/site/mods/599).

## Usage

Reinstaller adds tools to Mod Organizer's Tools menu: quick buttons for Create, Install, and Delete, plus the main Reinstaller menu.

### Create

Backs up a download file to Reinstaller:
1. Select a file from Mod Organizer's downloads folder
2. Optionally set a custom name
3. The file is backed up and can be safely deleted from downloads

### Install

Runs an installer from Reinstaller:
1. Select a mod from the list
2. If multiple files exist, select the specific file
3. The file is installed using Mod Organizer's install process

### Delete

Removes a file from Reinstaller:
1. Select a mod from the list
2. If multiple files exist, select the specific file
3. The file is deleted (removes the mod entry if it was the last file)

### Main Menu

![Reinstaller](img/reinstaller_installers.png)

The Reinstaller menu provides a browsable list of all backed up mods with options to add, install, and delete files.

## Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `enabled` | `true` | Enables or disables Reinstaller |

## Uninstallation

To remove Reinstaller, delete:
- `plugins\reinstaller\`
- `plugins\data\reinstaller\`

If Mod Organizer is at `C:\Mod Organizer\`, delete:
- `C:\Mod Organizer\plugins\reinstaller\`
- `C:\Mod Organizer\plugins\data\reinstaller\`
