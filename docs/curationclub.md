# Curation Club

Curation Club is a plugin for Mod Organizer 2 that allows users to import Creation Club content into Mod Organizer as separate mods.

## Features

- Organize Creation Club content directly within Mod Organizer
- Import all Creation Club content into Mod Organizer
- Customize names for Creation Club content
- Move Creation Club manifest files using Root Builder support

## Installation

Download Curation Club from [Nexus Mods](https://www.nexusmods.com/skyrimspecialedition/mods/60552) or [GitHub](https://github.com/Kezyma/ModOrganizer-Plugins/releases/tag/curationclub).

Extract the `curationclub` folder from the zip file and place it in Mod Organizer's plugins folder:
- Example: `C:\Mod Organizer\plugins\curationclub\`

Inside the folder you should find:
- A `shared` folder
- A `curationclub` folder
- A file called `__init__.py`

Curation Club will start the next time you run Mod Organizer.

Alternatively, install through [Plugin Finder](pluginfinder.md) or use the [Mod Organizer Setup Tool](https://www.nexusmods.com/site/mods/599).

## Usage

Open Curation Club from the Tools menu in Mod Organizer.

### How It Works

When run, Curation Club:
1. Searches the game folder and enabled mods in Mod Organizer
2. Finds any Creation Club content
3. Creates a new mod in Mod Organizer for each creation
4. Names each mod based on the configured format

### Configuration Options

- **Mod Name Format**: Customize how Creation Club mods are named using `{creation}` as a placeholder for the creation name
- **Root Builder Support**: Enable to also move Creation Club manifest files into Root folders with their respective mods

## Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `enabled` | `true` | Enables or disables Curation Club |
| `modnameformat` | `Creation Club - {creation}` | Format for Creation Club mod names. `{creation}` is replaced with the creation name |
| `rootbuildersupport` | `false` | Enables Root Builder support. Manifest files are moved to Root folders. Enable if using Root Builder, disable otherwise |

## Uninstallation

To remove Curation Club, delete:
- `plugins\curationclub\`
- `plugins\data\curationclub\`

If Mod Organizer is at `C:\Mod Organizer\`, delete:
- `C:\Mod Organizer\plugins\curationclub\`
- `C:\Mod Organizer\plugins\data\curationclub\`
