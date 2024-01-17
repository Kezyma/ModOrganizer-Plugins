@echo off

ECHO Stopping Mod Organizer
TASKKILL /F /IM ModOrganizer.exe > NUL

CD %~dp0

ECHO Generating UI for all plugins.
CALL "Generate UI.bat" > NUL

ECHO Building releases for all plugins.
CALL "Generate Release.bat" > NUL

CD %~dp0..\

IF EXIST debug\ (
	ECHO Mod Organizer is already installed.

) ELSE (
  	ECHO Mod Organizer is not installed.
	MKDIR temp

	ECHO Downloading https://www.7-zip.org/a/7zr.exe
	powershell -Command "(New-Object Net.WebClient).DownloadFile('https://www.7-zip.org/a/7zr.exe', 'temp\7zr.exe')"
	
	ECHO Downloading https://github.com/ModOrganizer2/modorganizer/releases/download/v2.5.0/Mod.Organizer-2.5.0.7z
	powershell -Command "(New-Object Net.WebClient).DownloadFile('https://github.com/ModOrganizer2/modorganizer/releases/download/v2.5.0/Mod.Organizer-2.5.0.7z', 'temp\Mod.Organizer-2.5.0.7z')"

	ECHO Installing Mod Organizer v2.5.0
	temp\7zr.exe x "temp\Mod.Organizer-2.5.0.7z" -o"%~dp0..\debug"

	RMDIR /S /Q temp
)

ECHO Deploying all plugins
FOR /d %%I IN (%~dp0..\release\*) DO (
	IF NOT "%%~nI" == "zip" (
		ECHO Deploying %%~nI
		CD "%~dp0..\"
		ROBOCOPY "release\%%~nI" "debug\plugins\%%~nI" /E > NUL
	)
)

ECHO Launching Mod Organizer
START %~dp0..\debug\ModOrganizer.exe


