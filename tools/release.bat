@echo off
cd /D "%~dp0\..\"

echo Removing existing release folder.
rmdir /S /Q "release"

echo Creating release folder.
mkdir "release"

echo Looping through mods.
for %%x in (%*) do (
	cd /D "%~dp0\..\"

	echo Creating %%x mod folder.
	mkdir "release\%%x"

	echo Copying %%x mod files to release folder.
	robocopy "src\plugin\%%x" "release\%%x\plugin\%%x" /E 
	robocopy "src\base" "release\%%x\base" /E 
	robocopy "src\common" "release\%%x\common" /E 
	robocopy "src" "release\%%x" "%%x_init.py" 

	echo Renaming %%x init file.
	ren "release\%%x\%%x_init.py" "__init__.py" 

	echo Creating zip folder.
	if not exist "release\zip" mkdir "release\zip" 

	echo Zipping %%x.
	cd /D "%~dp0\..\release" 
	tar.exe -a -cf "zip\%%x.zip" "%%x" 
)
