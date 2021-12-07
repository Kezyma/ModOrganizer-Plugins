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
	robocopy "src\%%x" "release\%%x\%%x" /E 
	robocopy "src\shared" "release\%%x\shared" /E 
	robocopy "src" "release\%%x" "%%x_init.py" 

	echo Renaming %%x init file.
	ren "release\%%x\%%x_init.py" "__init__.py" 

	
	echo Moving the readme files.
	robocopy "readme\%%x" "release\%%x" /E

	echo Creating zip folder.
	if not exist "release\zip" mkdir "release\zip" 

	echo Zipping %%x.
	cd /D "%~dp0\..\release" 
	tar.exe -a -cf "zip\%%x.zip" "%%x" 
)
