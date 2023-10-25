@echo off
cd /D "%~dp0\..\"

echo Removing existing release folder.
rmdir /S /Q "release"

echo Creating release folder.
mkdir "release"

echo Looping through mods.
FOR /d %%I IN (%~dp0..\src\plugin\*) DO (
    cd /D "%~dp0\..\"

	echo Creating %%~nI mod folder.
	mkdir "release\%%~nI"

	echo Copying %%~nI mod files to release folder.
	robocopy "src\plugin\%%~nI" "release\%%~nI\plugin\%%~nI" /E 
	robocopy "src\base" "release\%%~nI\base" /E 
	robocopy "src\common" "release\%%~nI\common" /E 
	robocopy "src" "release\%%~nI" "%%~nI_init.py" 

	echo Renaming %%~nI init file.
	ren "release\%%~nI\%%~nI_init.py" "__init__.py" 

	echo Creating zip folder.
	if not exist "release\zip" mkdir "release\zip" 

	echo Zipping %%~nI.
	cd /D "%~dp0\..\release" 
	tar.exe -a -cf "zip\%%~nI.zip" "%%~nI" 
)
