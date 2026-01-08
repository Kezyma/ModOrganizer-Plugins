@echo off
setlocal enabledelayedexpansion

REM ============================================================================
REM run_debug.bat - Build and run plugins in Mod Organizer debug environment
REM
REM This script:
REM   1. Checks if Mod Organizer is running (and stops it if so)
REM   2. Downloads and installs MO2 v2.5.2 if not present
REM   3. Runs build_debug.bat to build all plugins
REM   4. Deploys built plugins to debug\plugins\
REM   5. Launches Mod Organizer
REM ============================================================================

REM Get script directory
set "SCRIPT_DIR=%~dp0"
cd /D "%SCRIPT_DIR%"

echo.
echo ============================================================================
echo                     ModOrganizer-Plugins Debug Runner
echo ============================================================================
echo.

REM Step 1: Check if Mod Organizer is running
echo [1/5] Checking for running Mod Organizer instance...
tasklist /FI "IMAGENAME eq ModOrganizer.exe" 2>NUL | find /I /N "ModOrganizer.exe" >NUL
if "%ERRORLEVEL%"=="0" (
    echo   Mod Organizer is running. Stopping it...
    taskkill /F /IM ModOrganizer.exe >NUL 2>&1
    REM Wait a moment for process to fully terminate
    timeout /t 2 /nobreak >NUL
    echo   Stopped.
) else (
    echo   Mod Organizer is not running.
)

REM Step 2: Install Mod Organizer if needed
echo.
echo [2/5] Checking Mod Organizer installation...
if exist "debug\ModOrganizer.exe" (
    echo   Mod Organizer is already installed in debug\
) else (
    echo   Mod Organizer is not installed. Downloading v2.5.2...

    REM Create temp directory
    if not exist "temp" mkdir "temp"

    REM Download 7-Zip standalone
    echo   Downloading 7-Zip extractor...
    powershell -NoProfile -Command "(New-Object Net.WebClient).DownloadFile('https://www.7-zip.org/a/7zr.exe', 'temp\7zr.exe')"
    if not exist "temp\7zr.exe" (
        echo   ERROR: Failed to download 7zr.exe
        rmdir /S /Q "temp" 2>nul
        exit /b 1
    )

    REM Download Mod Organizer 2.5.2
    echo   Downloading Mod Organizer v2.5.2...
    powershell -NoProfile -Command "(New-Object Net.WebClient).DownloadFile('https://github.com/ModOrganizer2/modorganizer/releases/download/v2.5.2/Mod.Organizer-2.5.2.7z', 'temp\Mod.Organizer-2.5.2.7z')"
    if not exist "temp\Mod.Organizer-2.5.2.7z" (
        echo   ERROR: Failed to download Mod Organizer
        rmdir /S /Q "temp" 2>nul
        exit /b 1
    )

    REM Extract Mod Organizer
    echo   Extracting Mod Organizer to debug\...
    "temp\7zr.exe" x "temp\Mod.Organizer-2.5.2.7z" -o"debug" -y >NUL

    REM Cleanup temp
    rmdir /S /Q "temp"

    if exist "debug\ModOrganizer.exe" (
        echo   Installation complete.
    ) else (
        echo   ERROR: Installation failed.
        exit /b 1
    )
)

REM Step 3: Build all plugins
echo.
echo [3/5] Building all plugins...
echo.
call build_debug.bat nopause

if errorlevel 1 (
    echo.
    echo ERROR: Build failed. Aborting.
    exit /b 1
)

REM Step 4: Deploy plugins to debug installation
echo.
echo [4/5] Deploying plugins to debug\plugins\...

REM Ensure debug plugins directory exists
if not exist "debug\plugins" mkdir "debug\plugins"

REM Copy each plugin from release\plugins to debug\plugins
for /d %%I in (release\plugins\*) do (
    echo   Deploying %%~nI
    robocopy "release\plugins\%%~nI" "debug\plugins\%%~nI" /E /NFL /NDL /NJH /NJS /NC /NS /NP >NUL
)

echo   Deployment complete.

REM Step 5: Launch Mod Organizer
echo.
echo [5/5] Launching Mod Organizer...
start "" "%SCRIPT_DIR%debug\ModOrganizer.exe"

echo.
echo ============================================================================
echo Debug session started. Mod Organizer is now running.
echo ============================================================================
echo.

exit /b 0
