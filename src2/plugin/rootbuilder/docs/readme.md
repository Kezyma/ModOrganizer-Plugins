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
Root Builder has three primary functions; build, sync, and clear. By default, a build will run every time an application is launched through Mod Organizer and a clear is run when that application closes (or Mod Organizer is unlocked).

### Build
When a build runs, the following things happen;
- (Cache enabled) If no cache exists, all base game files (minus exclusions and the data folder) will be hashed and recorded.
- (Cache disabled) The names of base game files (minus exclusions and the data folder) will be recorded.
- (Backup enabled) If no backup exists, all base game files (minus exclusions and the data folder) will be backed up.
- (Backup disabled) Any base game files that would be overwritten by `Root` files are backed up.
- All files in `Root` folders are either copied or linked to the base game folder based on the current mode.
 
### Sync
When a sync runs, the following things happen;
- Any files from `Root` mods that have changed in the game folder are copied back to Mod Organizer.
- (Cache enabled) Any base game files that have changed are copied to Mod Organizer’s overwrite folder.
- Any new files in the base game folder are copied to Mod Organizer’s overwrite folder.
 
### Clear
When a clear runs, the following things happen;
- A sync is run.
- Any files copied or linked from `Root` folders are deleted.
- Any missing game files that were backed up are restored.
- (Backup disabled) Any backed up files are deleted.
- (Cache disabled) Any recorded base game file names and hashed are deleted.

# Configuration

## Mode
Root Builder has various modes that determine how files in `Root` folders are deployed to the game folder.

### Copy
Copy mode is enabled by default, in copy mode, any files found in `Root` folders are copied to the game folder during a build.

### Link
In link mode, any files found in `Root` folders have links created in the game folder during a build.

### USVFS
In usvfs mode, any files found in `Root` folders are mapped to the game folder using Mod Organizer’s VFS. This setting is often incompatible with any mods that contain `dll` or `exe` files.

### USVFS + Link
In usvfs + link mode, any files found in `Root` folders are mapped to the game folder using Mod Organizer’s VFS. Any `dll` or `exe` files found in `Root` folders will have links created instead to improve mod compatibility.

## Custom Mode
Instead of using the preset mode, you can define your own custom mode. With a custom mode you can control exactly which files are deployed from `Root` folders and which methods are used to deploy them.

### Rules
Each mode has a list of rules, these rules determine which files in `Root` folders use those methods. 
- Each rule should be the path to a file or folder, relative to the `Root` folder.
- Rules can contain the `**` wildcard which will match all files and folders.
- Rules can contain the `*` wildcard, which matches anything in a file or folder name.
- Any other wildcards supported by Python’s glob module should also function.

### Priority
Each deployment method has a priority. If a `Root` file matches the rules for multiple modes, the method with the lowest priority number is the one used. 

## Settings

### Backup
### Cache
### Autobuild
### Redirect
### Installer
### Debug

## Exclusions

# Troubleshooting