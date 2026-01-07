# Shortcutter

Shortcutter is a plugin for Mod Organizer 2 that allows users to create instance and profile-specific desktop shortcuts to launch applications through Mod Organizer.

## Features

- Create profile-specific shortcuts to launch apps with a specific profile
- Create instance-specific shortcuts that auto-switch to the correct instance (non-portable only)
- Pick custom icons for shortcuts
- Run different mod configurations without opening Mod Organizer

## Installation

Download Shortcutter from [Nexus Mods](https://www.nexusmods.com/skyrimspecialedition/mods/59827) or [GitHub](https://github.com/Kezyma/ModOrganizer-Plugins/releases/tag/shortcutter).

Extract the `shortcutter` folder from the zip file and place it in Mod Organizer's plugins folder:
- Example: `C:\Mod Organizer\plugins\shortcutter\`

Inside the folder you should find:
- A `shared` folder
- A `shortcutter` folder
- A file called `__init__.py`

Shortcutter will start the next time you run Mod Organizer.

Alternatively, install through [Plugin Finder](pluginfinder.md) or use the [Mod Organizer Setup Tool](https://www.nexusmods.com/site/mods/599).

## Usage

Open Shortcutter from the Tools menu in Mod Organizer.

![Shortcutter](img/shortcutter_shortcut.png)

### Creating a Shortcut

1. **Select Profile**: Choose the profile to use when the shortcut is launched
2. **Select Application**: Choose the executable to run from the current instance's executables list
3. **Select Icon**: Browse for an icon file (.ico) or executable (.exe) to use as the shortcut icon
4. **Name**: Enter a name for the shortcut

Click **OK** to create the shortcut on your desktop.

### Notes

- Instance-specific shortcuts only work with non-portable Mod Organizer installations
- The shortcut will launch the selected application through Mod Organizer with the specified profile active
- Custom icons are optional; the default application icon will be used if none is selected

## Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `enabled` | `true` | Enables or disables Shortcutter |

## Uninstallation

To remove Shortcutter, delete:
- `plugins\shortcutter\`
- `plugins\data\shortcutter\`

If Mod Organizer is at `C:\Mod Organizer\`, delete:
- `C:\Mod Organizer\plugins\shortcutter\`
- `C:\Mod Organizer\plugins\data\shortcutter\`
