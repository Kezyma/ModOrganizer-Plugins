# ModOrganizer-Plugins
Shared repository for [Mod Organizer](https://github.com/ModOrganizer2/modorganizer) plugins.

## Plugins

### [Root Builder](https://github.com/Kezyma/ModOrganizer-Plugins/blob/main/docs/rootbuilder.md)
Root Builder is a Mod Organizer 2 plugin that allows you to manage files in the base game folder through Mod Organizer, leaving your game folder in pristine, vanilla condition!

### [Reinstaller](https://github.com/Kezyma/ModOrganizer-Plugins/blob/main/docs/reinstaller.md)
Reinstaller is a Mod Organizer 2 plugin that allows you to backup downloaded mods and run their installers on demand. Useful for large fomod patch installers with loads of options that you have to re-run frequently. Don't let those files keep your downloads tab cluttered anymore!

### [Shortcutter](https://github.com/Kezyma/ModOrganizer-Plugins/blob/main/docs/shortcutter.md)
Shortcutter is a Mod Organizer 2 plugin that gives you the option of quickly creating instance and profile specific desktop shortcuts, allowing you to quickly launch your game using different profiles without having to manually switch inside Mod Organizer.

### [Plugin Finder](https://github.com/Kezyma/ModOrganizer-Plugins/blob/main/docs/pluginfinder.md)
Plugin Finder is a Mod Organizer 2 plugin that allows you to browse and install other plugins for Mod Organizer, as well as uninstall them.

### [Curation Club](https://github.com/Kezyma/ModOrganizer-Plugins/blob/main/docs/curationclub.md)
Curation Club is a plugin for Mod Organizer 2, allowing users to import Creation Club content into Mod Organizer as separate mods.

### [Profile Sync](https://github.com/Kezyma/ModOrganizer-Plugins/blob/main/docs/profilesync.md)
Profile Sync is a plugin for Mod Organizer 2, it allows you to maintain the same mod order (while keeping the enabled/disabled state) across multiple profiles.

### [OpenMW Player](https://github.com/Kezyma/ModOrganizer-Plugins/blob/main/docs/openmwplayer.md)
A plugin for Mod Organizer 2 that automatically exports your mod list, enabled plugins, and grass mods to OpenMW whenever you run the game through Mod Organizer. 

## Usage

### Installing Mods
To install a plugin from this repository, download a plugin from above and extract the folder inside into your `Mod Organizer\plugins` folder.

### This Repo
- `src` contains the plugin code and shared code folders. Each plugin has its own folder and a `plugin_init.py` file.
- `release` contains the plugins packaged for individual release. each folder is an individual plugin.
- `directory` contains the plugin directory used by Plugin Finder to search and install plugins.
- `meta` contains meta files for the NexusMods downloads, to be used when creating Wabbajack lists.
- `tools` contains various batch files.

### Tools

The `tools` folder contains build scripts and utilities. All scripts can be run from any directory.

Version format is `x.y.z` (major.minor.build).

#### Build Scripts

| Script | Description |
|--------|-------------|
| `build.bat` | Interactive mode: select plugins to build |
| `build.bat <plugin> [plugin2] ...` | Build specified plugin(s) using current version |
| `build.bat all` | Build all plugins |
| `build_all.bat` | Build all plugins (same as `build.bat all`) |

Build scripts:
- Generate UI files for PyQt5 and PyQt6
- Copy plugin files to `release\plugins\<pluginname>`
- Create versioned zip in `release\<pluginname>\<pluginname>.<version>.zip`

#### Debug Scripts

| Script | Description |
|--------|-------------|
| `debug.bat` | Interactive mode: select plugins to build and launch MO2 |
| `debug.bat <plugin> [plugin2] ...` | Build specified plugin(s) and launch MO2 |
| `debug.bat all` | Build all plugins and launch MO2 |
| `debug_all.bat` | Build all plugins and launch MO2 (same as `debug.bat all`) |

Debug scripts:
- Stop any running MO2 instance
- Download and install MO2 v2.5.2 to `debug\` if not present
- Build specified plugins
- Deploy built plugins to `debug\plugins\`
- Launch MO2

#### Version Scripts

| Script | Description | Example |
|--------|-------------|---------|
| `inc_version.bat` | Interactive mode: select plugins | 1.2.5 -> 1.3.0 |
| `inc_version.bat <plugin> [plugin2] ...` | Increment minor (Y), reset build (Z) | 1.2.5 -> 1.3.0 |
| `inc_build.bat` | Interactive mode: select plugins | 1.2.5 -> 1.2.6 |
| `inc_build.bat <plugin> [plugin2] ...` | Increment build (Z) | 1.2.5 -> 1.2.6 |

All scripts support `all` as an argument to process all plugins.

#### Typical Workflow

```batch
REM During development - just rebuild and test
tools\debug.bat rootbuilder

REM Before a release - increment version, build, and test
tools\inc_version.bat rootbuilder
tools\debug.bat rootbuilder

REM Quick fix - increment build number
tools\inc_build.bat rootbuilder
tools\build.bat rootbuilder
```

#### Other Utilities

| File | Description |
|------|-------------|
| `Generate UI.bat` | Converts `.ui` files to Python for PyQt5 and PyQt6. |
| `Generate Release.bat` | Legacy: deploys all plugins from `src` to `release`. |
| `Launch Debug.bat` | Legacy: generates UI, release, downloads MO2, launches for testing. |
| `MetaGenerator.exe` | Generates NexusMods meta files for Wabbajack list authors. |