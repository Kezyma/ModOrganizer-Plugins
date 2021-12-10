# Reinstaller
## v1.0.*

### Introduction
Reinstaller allows you to conveninetly backup mod installers to re-run later, without risk of them cluttering up your downloads section in Mod Organizer 2.

### Installation
Copy the reinstaller folder to Mod Organizer's plugins folder. If Mod Organizer is installed at `D:\MO\`, the plugins folder will be located at `D:\MO\plugins\`
Make sure that `__init__.py` is located at `D:\MO\plugins\reinstaller\` and not directly copied into the plugins folder itself.

### Uninstallation
Delete the following folders from Mod Organizer, assuming Mod Organizer is installed at `D:\MO\`:
`D:\MO\plugins\reinstaller\`
`D:\MO\plugins\data\reinstaller\`

### Usage
A new item will appear in the tools menu of Mod Organizer with the three main functions of Reinstaller, install, create and delete.

*Reinstaller menu item*

![Reinstaller menu item](reinstaller_tool_menu.png "Reinstaller menu item")

### Reinstaller
The Reinstaller option will open a manager window for easily managing backed up installers.

*Reinstaller window*

![Reinstaller window](reinstaller_window.png "Reinstaller window")

#### Create
Takes a backup of a file from your current downloads folder and stores it.

#### Install
Lists all the currently backed up installers, when you select one, it will be installed through Mod Organizer 2.

#### Delete
Lists all the currently backed up installers, when you select one, it will be deleted.

### Settings

#### enabled (default: true)
Determines whether the Reinstaller plugin is enabled in Mod Organizer.

## Other Plugins
#### [Root Builder](https://www.nexusmods.com/skyrimspecialedition/mods/31720), [Reinstaller](https://www.nexusmods.com/skyrimspecialedition/mods/59292), [Shortcutter](https://www.nexusmods.com/skyrimspecialedition/mods/59827)