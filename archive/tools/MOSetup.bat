@ECHO OFF

ECHO Checking for existing temp folder and deleting.
cd "%~dp0"
rmdir /Q /S temp

ECHO Creating new temp folder.
cd "%~dp0"
mkdir temp

cd "%~dp0temp"
ECHO Downloading Plugin Filder v1.2.4
powershell -Command "Invoke-WebRequest https://github.com/Kezyma/ModOrganizer-Plugins/releases/download/pluginfinder/pluginfinder.1.2.4.zip -OutFile pluginfinder.zip"
ECHO Downloading Reinstaller v1.1.1
powershell -Command "Invoke-WebRequest https://github.com/Kezyma/ModOrganizer-Plugins/releases/download/reinstaller/reinstaller.1.1.1.zip -OutFile reinstaller.zip"
ECHO Downloading Root Builder v4.4.2
powershell -Command "Invoke-WebRequest https://github.com/Kezyma/ModOrganizer-Plugins/releases/download/rootbuilder/rootbuilder.4.4.2.zip -OutFile rootbuilder.zip"
ECHO Downloading Shortcutter v1.1.0
powershell -Command "Invoke-WebRequest https://github.com/Kezyma/ModOrganizer-Plugins/releases/download/shortcutter/shortcutter.1.1.0.zip -OutFile shortcutter.zip"
ECHO Downloading Curation Club v1.1.0
powershell -Command "Invoke-WebRequest https://github.com/Kezyma/ModOrganizer-Plugins/releases/download/curationclub/curationclub.1.1.0.zip -OutFile curationclub.zip"
ECHO Downloading Profile Sync v.1.1.1
powershell -Command "Invoke-WebRequest https://github.com/Kezyma/ModOrganizer-Plugins/releases/download/profilesync/profilesync.1.1.1.zip -OutFile profilesync.zip"
ECHO Downloading OpenMW Player v0.0.10
powershell -Command "Invoke-WebRequest https://github.com/Kezyma/ModOrganizer-Plugins/releases/download/openmwplayer/openmwplayer.0.0.10.zip -OutFile openmwplayer.zip"

ECHO Extracting Plugin Finder
powershell -Command "Expand-Archive pluginfinder.zip"
ECHO Extracting Reinstaller
powershell -Command "Expand-Archive reinstaller.zip"
ECHO Extracting Root Builder
powershell -Command "Expand-Archive rootbuilder.zip"
ECHO Extracting Shortcutter
powershell -Command "Expand-Archive shortcutter.zip"
ECHO Extracting Curation Club
powershell -Command "Expand-Archive curationclub.zip"
ECHO Extracting Profile Sync
powershell -Command "Expand-Archive profilesync.zip"
ECHO Extracting OpenMW Player
powershell -Command "Expand-Archive openmwplayer.zip"

ECHO Downloading Mod Organizer 2 v2.4.4
powershell -Command "Invoke-WebRequest https://github.com/ModOrganizer2/modorganizer/releases/download/v2.4.4/Mod.Organizer-2.4.4.7z -OutFile modorganizer.7z"

ECHO Extracting Mod Organizer 2
cd "%~dp0temp"
echo f | xcopy /f /y "%~dp0temp\pluginfinder\pluginfinder\pluginfinder\modules\7za.exe" "%~dp0temp\7za.exe"
cd "%~dp0temp"
call 7za.exe x "%~dp0temp\modorganizer.7z" -o"%~dp0temp\ModOrganizer"

ECHO Moving Plugins.
move "%~dp0temp\pluginfinder\pluginfinder" "%~dp0temp\ModOrganizer\plugins\"
move "%~dp0temp\reinstaller\reinstaller" "%~dp0temp\ModOrganizer\plugins\"
move "%~dp0temp\rootbuilder\rootbuilder" "%~dp0temp\ModOrganizer\plugins\"
move "%~dp0temp\shortcutter\shortcutter" "%~dp0temp\ModOrganizer\plugins\"
move "%~dp0temp\curationclub\curationclub" "%~dp0temp\ModOrganizer\plugins\"
move "%~dp0temp\profilesync\profilesync" "%~dp0temp\ModOrganizer\plugins\"
move "%~dp0temp\openmwplayer\openmwplayer" "%~dp0temp\ModOrganizer\plugins\"

ECHO Moving Mod Organizer.
move "%~dp0temp\ModOrganizer" "%~dp0"

ECHO Cleaning up temp folder.
cd "%~dp0"
rmdir /Q /S temp
