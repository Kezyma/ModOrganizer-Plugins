# Plugin Finder

Plugin Finder is a plugin for Mod Organizer 2 that allows users to browse and install other Mod Organizer plugins.

## Features

- Browse a list of plugins and search by name
- Install plugins directly within Mod Organizer
- Check for updates to installed plugins
- Remove plugins from within Plugin Finder

> **Note:** Plugins found within Plugin Finder are produced and maintained by independent mod authors and may vary in quality. Issues with plugins should be directed to the respective plugin author.

## Installation

Download Plugin Finder from [Nexus Mods](https://www.nexusmods.com/skyrimspecialedition/mods/59869) or [GitHub](https://github.com/Kezyma/ModOrganizer-Plugins/releases/tag/pluginfinder).

Extract the `pluginfinder` folder from the zip file and place it in Mod Organizer's plugins folder:
- Example: `C:\Mod Organizer\plugins\pluginfinder\`

Inside the folder you should find:
- A `shared` folder
- A `pluginfinder` folder
- A file called `__init__.py`

Plugin Finder will start the next time you run Mod Organizer.

Alternatively, use the [Mod Organizer Setup Tool](https://www.nexusmods.com/site/mods/599) to install Mod Organizer with Plugin Finder included.

## Usage

Open Plugin Finder from the Tools menu in Mod Organizer.

![Plugin Finder](img/pluginfinder_finder.png)

The browser displays available plugins with the following information:

### Status Icons

- **Download count**: Total installs through Plugin Finder (minus uninstalls)
- **Release type**:
  - Alpha: Plugin is in early development
  - Beta: Plugin is in testing phase
  - RC (Release Candidate): Plugin is nearly ready for release
- **Install status**:
  - Checkmark: Installed and up to date
  - Warning: May not work on this Mod Organizer version
  - Stop: Does not work on this Mod Organizer version
  - Info: Cannot be installed through Plugin Finder
  - Update available: New version ready to install
  - Update warning: Update available but may not work on this version
  - Update blocked: Update available but incompatible with this version

### Actions

- **Install**: Install the selected plugin
- **Uninstall**: Remove the selected plugin
- **Documentation**: Visit the plugin's documentation
- **Nexus**: Visit the plugin's Nexus page
- **GitHub**: Visit the plugin's GitHub page

Use the search box to filter plugins by name. Navigation buttons allow paging through results and refreshing the plugin list.

## Adding Your Plugin

To add your plugin to Plugin Finder, create a JSON manifest file containing plugin information and version details.

### Using the Generator

The easiest way to create a manifest is using the [Plugin Finder JSON Generator](https://kezyma.github.io/index.html?p=pluginfinder-generator).

### Manual Creation

Create a JSON file with the following structure:

```json
{
  "Name": "Plugin Name",
  "Author": "Your Name",
  "Description": "Short description (max 350 characters)",
  "DocsUrl": "https://example.com/docs",
  "NexusUrl": "https://www.nexusmods.com/...",
  "GithubUrl": "https://github.com/...",
  "Versions": [
    {
      "Version": "1.0.0",
      "Released": "2024-01-15",
      "MinSupport": "2.4.2",
      "MaxSupport": "2.5.0",
      "MinWorking": "",
      "MaxWorking": "",
      "ReleaseNotes": ["Initial release"],
      "DownloadUrl": "https://github.com/.../plugin.1.0.0.zip",
      "PluginPath": ["pluginname"],
      "LocalePath": [],
      "DataPath": ["data/pluginname"]
    }
  ]
}
```

### Plugin Fields

| Field | Required | Description |
|-------|----------|-------------|
| `Name` | Yes | Display name (should not change once added) |
| `Author` | Yes | Author name to display |
| `Description` | No | Short description (max 350 characters) |
| `DocsUrl` | No | URL to documentation |
| `NexusUrl` | No | URL to Nexus page |
| `GithubUrl` | No | URL to GitHub page |
| `Versions` | No | Array of installable versions |

### Version Fields

| Field | Required | Description |
|-------|----------|-------------|
| `Version` | Yes | Version number (matching MO2 settings display format) |
| `Released` | Yes | Release date (yyyy-MM-dd format) |
| `MinSupport` | No | Minimum tested MO2 version (warning shown for earlier) |
| `MaxSupport` | No | Maximum tested MO2 version (warning shown for later) |
| `MinWorking` | No | Minimum working MO2 version (blocks earlier) |
| `MaxWorking` | No | Maximum working MO2 version (blocks later) |
| `ReleaseNotes` | No | Array of release notes |
| `DownloadUrl` | Yes | Direct download URL to the zip file |
| `PluginPath` | Yes | Paths in zip to copy to plugins folder |
| `LocalePath` | No | Paths in zip to copy to translations folder |
| `DataPath` | No | Paths to delete on uninstall (relative to plugins folder) |

### Submitting Your Plugin

Host your JSON file on GitHub with your plugin, then submit it to Plugin Finder:

1. Open a pull request editing [plugin_directory.json](https://github.com/Kezyma/ModOrganizer-Plugins/blob/main/directory/plugin_directory.json)
2. Open an [issue](https://github.com/Kezyma/ModOrganizer-Plugins/issues) with your plugin name and JSON URL
3. Contact Kezyma on Discord: `Kezyma#7969`

## Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `enabled` | `true` | Enables or disables Plugin Finder |
| `priority` | `120` | Priority of the installer module for installing plugins |

## Uninstallation

To remove Plugin Finder, delete:
- `plugins\pluginfinder\`
- `plugins\data\pluginfinder\`

If Mod Organizer is at `C:\Mod Organizer\`, delete:
- `C:\Mod Organizer\plugins\pluginfinder\`
- `C:\Mod Organizer\plugins\data\pluginfinder\`
