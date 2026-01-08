@echo off
setlocal enabledelayedexpansion

REM ============================================================================
REM build.bat - Shared build script for ModOrganizer-Plugins
REM
REM Usage: build.bat <plugin_name> <new_version>
REM   plugin_name: Name of the plugin (e.g., rootbuilder, profilesync)
REM   new_version: Version string in format x.y.z
REM
REM This script:
REM   1. Updates the plugin version in the plugin file
REM   2. Generates UI files for PyQt5 and PyQt6
REM   3. Copies plugin files to release\plugins\<plugin_name>
REM   4. Creates a versioned zip file at release\<plugin_name>.<version>.zip
REM ============================================================================

REM Get script directory
set "SCRIPT_DIR=%~dp0"
cd /D "%SCRIPT_DIR%"

REM Validate arguments
if "%~1"=="" (
    echo ERROR: Plugin name is required.
    echo Usage: build.bat ^<plugin_name^> ^<new_version^>
    exit /b 1
)
if "%~2"=="" (
    echo ERROR: Version is required.
    echo Usage: build.bat ^<plugin_name^> ^<new_version^>
    exit /b 1
)

set "PLUGIN_NAME=%~1"
set "NEW_VERSION=%~2"

REM Parse version components
for /f "tokens=1,2,3 delims=." %%a in ("%NEW_VERSION%") do (
    set "VER_X=%%a"
    set "VER_Y=%%b"
    set "VER_Z=%%c"
)

echo.
echo ============================================================================
echo Building %PLUGIN_NAME% version %NEW_VERSION%
echo ============================================================================

REM Check if plugin exists
if not exist "src\plugin\%PLUGIN_NAME%" (
    echo ERROR: Plugin '%PLUGIN_NAME%' not found in src\plugin\
    exit /b 1
)

REM Step 1: Update version in plugin file
echo.
echo [1/4] Updating version to %NEW_VERSION%...
set "PLUGIN_FILE=src\plugin\%PLUGIN_NAME%\core\%PLUGIN_NAME%_plugin.py"

if not exist "%PLUGIN_FILE%" (
    echo ERROR: Plugin file not found: %PLUGIN_FILE%
    exit /b 1
)

REM Update version using PowerShell directly (avoids batch escaping issues)
powershell -NoProfile -ExecutionPolicy Bypass -Command "$f='%PLUGIN_FILE%'; $c=Get-Content $f -Raw; $c=$c -replace 'mobase\.VersionInfo\s*\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\)','mobase.VersionInfo(%VER_X%, %VER_Y%, %VER_Z%)'; Set-Content $f -Value $c -NoNewline"

if errorlevel 1 (
    echo ERROR: Failed to update version in plugin file.
    exit /b 1
)
echo Version updated successfully.

REM Step 2: Generate UI files
echo.
echo [2/4] Generating UI files...
set "UI_DIR=src\plugin\%PLUGIN_NAME%\ui"

if exist "%UI_DIR%" (
    for /R "%UI_DIR%" %%G in (*.ui) do (
        echo   Processing %%~nxG

        REM Create output directories if they don't exist
        if not exist "%%~dpGqt5" mkdir "%%~dpGqt5"
        if not exist "%%~dpGqt6" mkdir "%%~dpGqt6"

        REM Generate for PyQt6
        python -m PyQt6.uic.pyuic "%%G" -o "%%~dpGqt6\%%~nG.py" 2>nul
        if errorlevel 1 (
            echo   Warning: PyQt6 generation failed for %%~nxG
        )

        REM Generate for PyQt5
        python -m PyQt5.uic.pyuic "%%G" -o "%%~dpGqt5\%%~nG.py" 2>nul
        if errorlevel 1 (
            echo   Warning: PyQt5 generation failed for %%~nxG
        )
    )
) else (
    echo   No UI directory found, skipping UI generation.
)

REM Step 3: Copy files to release directory
echo.
echo [3/4] Copying files to release\plugins\%PLUGIN_NAME%...

REM Create plugins directory if it doesn't exist
if not exist "release\plugins" mkdir "release\plugins"

REM Remove existing plugin folder
if exist "release\plugins\%PLUGIN_NAME%" (
    rmdir /S /Q "release\plugins\%PLUGIN_NAME%"
)
mkdir "release\plugins\%PLUGIN_NAME%"

REM Copy plugin files
robocopy "src\plugin\%PLUGIN_NAME%" "release\plugins\%PLUGIN_NAME%\plugin\%PLUGIN_NAME%" /E /NFL /NDL /NJH /NJS /NC /NS /NP >nul
robocopy "src\base" "release\plugins\%PLUGIN_NAME%\base" /E /NFL /NDL /NJH /NJS /NC /NS /NP >nul
robocopy "src\common" "release\plugins\%PLUGIN_NAME%\common" /E /NFL /NDL /NJH /NJS /NC /NS /NP >nul

REM Copy and rename init file
if exist "src\%PLUGIN_NAME%_init.py" (
    copy "src\%PLUGIN_NAME%_init.py" "release\plugins\%PLUGIN_NAME%\__init__.py" >nul
) else (
    echo WARNING: Init file not found: src\%PLUGIN_NAME%_init.py
)

echo Files copied successfully.

REM Step 4: Create zip file
echo.
echo [4/4] Creating release\%PLUGIN_NAME%.%NEW_VERSION%.zip...

REM Remove existing zip if it exists
if exist "release\%PLUGIN_NAME%.%NEW_VERSION%.zip" (
    del "release\%PLUGIN_NAME%.%NEW_VERSION%.zip"
)

REM Create zip using tar (built into Windows 10+)
cd "release\plugins"
tar.exe -a -cf "..\%PLUGIN_NAME%.%NEW_VERSION%.zip" "%PLUGIN_NAME%" 2>nul
cd "%SCRIPT_DIR%"

if exist "release\%PLUGIN_NAME%.%NEW_VERSION%.zip" (
    echo Zip created successfully.
) else (
    echo ERROR: Failed to create zip file.
    exit /b 1
)

echo.
echo Build complete: %PLUGIN_NAME% v%NEW_VERSION%
echo ============================================================================

exit /b 0
