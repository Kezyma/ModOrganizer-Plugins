# ModOrganizer-Plugins
Shared repository for [Mod Organizer](https://github.com/ModOrganizer2/modorganizer) plugins.

## Plugins

### [Root Builder](https://kezyma.github.io/?p=rootbuilder)
Root Builder is a Mod Organizer 2 plugin that allows you to manage files in the base game folder through Mod Organizer, leaving your game folder in pristine, vanilla condition!

### [Reinstaller](https://kezyma.github.io/?p=reinstaller)
Reinstaller is a Mod Organizer 2 plugin that allows you to backup downloaded mods and run their installers on demand. Useful for large fomod patch installers with loads of options that you have to re-run frequently. Don't let those files keep your downloads tab cluttered anymore!

### [Shortcutter](https://kezyma.github.io/?p=shortcutter)
Shortcutter is a Mod Organizer 2 plugin that gives you the option of quickly creating instance and profile specific desktop shortcuts, allowing you to quickly launch your game using different profiles without having to manually switch inside Mod Organizer.

### [Plugin Finder](https://kezyma.github.io/?p=pluginfinder)
Plugin Finder is a Mod Organizer 2 plugin that allows you to browse and install other plugins for Mod Organizer, as well as uninstall them.

### [Curation Club](https://kezyma.github.io/?p=curationclub)
Curation Club is a plugin for Mod Organizer 2, allowing users to import Creation Club content into Mod Organizer as separate mods.

### [Profile Sync](https://kezyma.github.io/?p=profilesync)
Profile Sync is a plugin for Mod Organizer 2, it allows you to maintain the same mod order (while keeping the enabled/disabled state) across multiple profiles.

### [OpenMW Player](https://kezyma.github.io/?p=openmwplayer)
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
the `tools` folder contains a few batch files.


#### Generate Release.bat
When run, will deploy all plugins from the `src` folder to the `release` folder as well as zip them up and store them in `release\zip`.

#### Generate UI.bat
When run, will search the `src` folder for `ui` files alongside `qt5` and `qt6` folders, then convert those files to python for each version of PyQt. Requires PyQt5 and PyQt6 to be installed.

#### Launch Debug.bat
When run, will generate UI and a release with `Generate UI.bat` and `Generate Release.bat`, then download Mod Organizer 2 (if not already downloaded), install it in a folder called `debug`, deploy all plugins to it and launch `ModOrganizer.exe` for testing.

#### MetaGenerator.exe
When run, will check NexusMods for each plugin listed in `Plugins.json` and generate a file in the `meta` folder for Wabbajck list authors to use.