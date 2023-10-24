# Using Root Builder

## The Root Folder
The `Root` folder is a special folder that can be added to a mod. Any files inside the `Root` folder are managed by Root Builder and will be deployed to the base game folder when a build happens.

`Root` folders must be at the top level of the mod and a mod can have both a `Root` folder as well as other folders and files which are handled by Mod Organizer normally, such as `Textures` or `Meshes`.

![Example Root Folder](img\root_folder.jpg)

## Installing Mods
To install a mod that has files which need to go inside the game folder, install it through Mod Organizer and use the manual option when installing.

![Example Mod Install Before](img\install_before.jpg)

Create a `Root` folder at the top level and move any files that need deploying to the game folder into it. If there are any other folders that Mod Organizer can manage normally, move them alongside the `Root` folder.

![Example Mod Install After](img\install_after.jpg)

If a mod only contains a `Root` folder, Mod Organizer will warn you that the mod does not appear valid, this can be safely ignored.

## Build, Sync & Clear

### Build
### Sync
### Clear

# Configuration

## Mode

### Copy
### Link
### USVFS
### USVFS + Link

## Custom Mode

## Settings

### Backup
### Cache
### Autobuild
### Redirect
### Installer
### Debug

## Exclusions

# Troubleshooting