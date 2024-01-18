@echo off
CD /D %~dp0

ECHO Deleting existing release.
RMDIR /S /Q "..\release"

ECHO Creating new release directory.
MKDIR "..\release"

ECHO Searching for plugins.
ECHO %~dp0
FOR /d %%I IN (%~dp0..\src\plugin\*) DO (
	ECHO Creating release for %%~nI.
	MKDIR "..\release\%%~nI"

	ECHO Copying plugin files into release.
	CD "%~dp0..\"
	ROBOCOPY "src\plugin\%%~nI" "release\%%~nI\plugin\%%~nI" /E 
	ROBOCOPY "src\base" "release\%%~nI\base" /E 
	ROBOCOPY "src\common" "release\%%~nI\common" /E 
	ROBOCOPY "src" "release\%%~nI" "%%~nI_init.py" 

	ECHO Renaming plugin init file.
	CD "%~dp0..\"
	REN "release\%%~nI\%%~nI_init.py" "__init__.py" 

	ECHO Zipping released mods.
	IF NOT EXIST "release\zip" MKDIR "release\zip"

	ECHO Zipping %%~nI.
	CD "%~dp0..\release"
	tar.exe -a -cf "zip\%%~nI.zip" "%%~nI" 
)