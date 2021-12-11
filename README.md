# ModOrganizer-Plugins
Shared repository for [Mod Organizer](https://github.com/ModOrganizer2/modorganizer) plugins.

## Plugins

### [Root Builder](/release/rootbuilder)
[Nexus](https://www.nexusmods.com/skyrimspecialedition/mods/31720), 
[Download](https://github.com/Kezyma/ModOrganizer-Plugins/releases/download/Current/rootbuilder.zip)

Root Builder is a Mod Organizer 2 plugin that allows you to manage files in the base game folder through Mod Organizer, leaving your game folder in pristine, vanilla condition!

### [Reinstaller](/release/reinstaller)
[Nexus](https://www.nexusmods.com/skyrimspecialedition/mods/59292)

Reinstaller is a Mod Organizer 2 plugin that allows you to backup downloaded mods and run their installers on demand. Useful for large fomod patch installers with loads of options that you have to re-run frequently. Don't let those files keep your downloads tab cluttered anymore!

### [Shortcutter](/release/shortcutter)
[Nexus](https://www.nexusmods.com/skyrimspecialedition/mods/59827)

Shortcutter is a Mod Organizer 2 plugin that gives you the option of quickly creating instance and profile specific desktop shortcuts, allowing you to quickly launch your game using different profiles without having to manually switch inside Mod Organizer.

### [Plugin Finder](/release/pluginfinder)

Plugin Finder is a Mod Organizer 2 plugin that allows you to browse and install other plugins for Mod Organizer, as well as uninstall them.

## Usage

### Installing Mods
To install a plugin from this repository, copy a folder from [`release`](/release/) into your `Mod Organizer\plugins` folder.

To install all plugins, rename the `src` folder and copy it into your `Mod Organizer\plugins` folder.

### This Repo
- `src` contains the plugin code and a shared code folder. Each plugin has its own folder and a `plugin_init.py` file.
- `release` contains the plugins packaged for individual release. each folder is an individual plugin.
- `readme` contains the readme files (and any other documentation) in individual plugin folders.
- `tools` contains various batch files.

### Tools
the `tools` folder contains a few batch files.

#### cleanup.bat
When called, the `release` folder will be deleted, as will any log files in the `tools` folder.

#### release.bat
Calling release.bat with parameters of different plugin names will; (eg. `release.bat rootbuilder reinstaller` would build rootbuilder and reinstaller)
- Copy the plugin and shared folders from `src` to `release\plugin`
- Copy the `plugin_init.py` file to `release\plugin` and rename it to `__init__.py`
- Copy the readme content from `readme\plugin` to `release\plugin`
- Zip the plugin for release and place it in `release\zip`

#### release_all.bat
Calls release.bat with parameters for every plugin.

#### deploy.bat
Calling deploy.bat with parameters of different plugin names will copy the relevant plugin folder from `release` to all the folders listed in `deploy_targets.txt`
(eg. `deploy.bat rootbuilder reinstaller` would deploy rootbuilder and reinstaller)

#### deploy_all.bat
Calls deploy.bat with parameters for every plugin.
