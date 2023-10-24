Root Builder is a plugin for Mod Organizer that allows you to manage files in the game folder that are not covered by Mod Organizer. By arranging mods so that files go into a folder named `Root`, those files will be deployed to the game folder for you.


# Using Root Builder

![Fig 1](fig_1.png)


## Installing Mods
When you are installing a mod that has files which need to go into the game folder, use the manual option to rearrange the files yourself.

Create a folder at the top level and name it `Root`, then move any files that you want into this folder. These files will be deployed directly to the game folder.

You can arrange any other files in this mod as they normally should be for Mod Organizer if not everything in the mod needs to be deployed.


## Build, Sync & Clear
Root Builder has three primary functions; Build, Sync & Clear. 

By default, a build will run every time an application is launched through Mod Organizer and a clear will run when that application closes.

### Build
When a build is run, the following things happen, differences based on settings are listed;
- (Cache on) If the base game has not been hashed yet, each file is hashed and recorded.
- (Cache off) The names of files in the base game are recorded.
- (Backup on) If the base game has not been backed up yet, the game files are backed up.
- (Backup off) If there are any base game files about to be overwritten, they are backed up.
- Depending on your mode options, files in `Root` folders are either copied or linked to the game folder.

### Sync
When a sync is run, each file in the game folder is checked for changes;
- If a file from a mod has changed, the new file is copied back to Mod Organizer.
- If a file from the base game has changed, the new file is copied to Mod Organizer's overwrite folder.
- If a file is not from a mod, or from the base game, it is copied to Mod Organizer's overwrite folder.

### Clear
When a clear is run, the following things happen, differences based on settings are listed;
- A sync is run.
- Any files copied or linked to the game folder are removed.
- Any missing game files are restored from backup.
- (Backup off) Any files that were backed up are deleted.
- (Cache off) Any cache of base game file names or hashes is deleted.


# Configuration Options


## Modes
### Copy (default)
When copy mode is enabled, any files found in `Root` folders will be copied to the game folder during a build. The copied files are then removed during a clear.

### Link
When copy mode is enabled, any files found in `Root` folders will have links created the game folder during a build. They are then unlinked during a clear.

### USVFS
When USVFS mode is enabled, any files found in `Root` folders will be mapped to the game folder using Mod Organizer's VFS. This is often incompatible with some mods.

### USVFS + Link
When USVFS + Link mode is enabled, any files found in `Root` folders will be mapped to the game folder using Mod Organizer's VFS. Any `dll` or `exe` files found in `Root` folders will have links created for them during a build to increase compatibility with some mods.


## Custom Mode
Setting a custom mode lets you control how Root Builder will deploy each individual file.
- The Custom tab has three sections, one each for files that should be copied, linked or handled through USVFS. 
- Any file or folder found in a `Root` folder that matches a file listed here will be deployed through that method.
- File or folder paths entered should be relative to the `Root` folder.
- These settings support wildcards, notably `**` for all subfolders and files, and `*` to match anything in a path.
- Any other wildcards that work with Python's glob module should work here.
- Each method has a priority. If a file is in both lists, the one with the lower priority is how that file is deployed. 

Some examples for what can be entered;
- `**` - match every file in `Root` folders.
- `**\*.exe` - match every `exe` file found in `Root` folders.
- `**\mwse.exe` - match every `mwse.exe` found in `Root` folders.
- `mwse.exe` - match `mwse.exe` in the top level of `Root` folders.
- `mcpatch` or `mcpatch\**` - match the `mcpatch` folder in the top level of `Root` folders.


## Settings
- Backup
If backup is enabled, when a build runs, any game files (not matching the exclusions or in the data folder) are backed up and will be restored on the next clear. If backup is disabled, only files that would be overwritten by a copied or linked file are backed up.
- Cache
- Autobuild
- Redirect
- Installer
- Debug

## Exclusions

# Troubleshooting