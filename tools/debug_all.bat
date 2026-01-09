@echo off
setlocal enabledelayedexpansion

REM ============================================================================
REM debug_all.bat - Build all plugins and launch Mod Organizer for testing
REM
REM Usage: debug_all.bat
REM
REM This script:
REM   1. Stops any running Mod Organizer instance
REM   2. Downloads and installs MO2 v2.5.2 if not present
REM   3. Builds all plugins
REM   4. Deploys all plugins to debug\plugins\
REM   5. Launches Mod Organizer
REM ============================================================================

REM Get script directory and change to repo root
set "SCRIPT_DIR=%~dp0"
cd /D "%SCRIPT_DIR%.."

echo.
echo ============================================================================
echo                     Debug Runner (All Plugins)
echo ============================================================================

REM Step 1: Check if Mod Organizer is running
echo.
echo [1/4] Checking for running Mod Organizer instance...
tasklist /FI "IMAGENAME eq ModOrganizer.exe" 2>NUL | find /I /N "ModOrganizer.exe" >NUL
if "%ERRORLEVEL%"=="0" (
    echo   Stopping Mod Organizer...
    taskkill /F /IM ModOrganizer.exe >NUL 2>&1
    timeout /t 2 /nobreak >NUL
    echo   Stopped.
) else (
    echo   Not running.
)

REM Step 2: Install Mod Organizer if needed
echo.
echo [2/4] Checking Mod Organizer installation...
if exist "debug\ModOrganizer.exe" (
    echo   Already installed.
) else (
    echo   Downloading Mod Organizer v2.5.2...

    if not exist "temp" mkdir "temp"

    echo   Downloading 7-Zip extractor...
    powershell -NoProfile -Command "(New-Object Net.WebClient).DownloadFile('https://www.7-zip.org/a/7zr.exe', 'temp\7zr.exe')"
    if not exist "temp\7zr.exe" (
        echo   ERROR: Failed to download 7zr.exe
        rmdir /S /Q "temp" 2>nul
        exit /b 1
    )

    echo   Downloading Mod Organizer...
    powershell -NoProfile -Command "(New-Object Net.WebClient).DownloadFile('https://github.com/ModOrganizer2/modorganizer/releases/download/v2.5.2/Mod.Organizer-2.5.2.7z', 'temp\Mod.Organizer-2.5.2.7z')"
    if not exist "temp\Mod.Organizer-2.5.2.7z" (
        echo   ERROR: Failed to download Mod Organizer
        rmdir /S /Q "temp" 2>nul
        exit /b 1
    )

    echo   Extracting...
    "temp\7zr.exe" x "temp\Mod.Organizer-2.5.2.7z" -o"debug" -y >NUL
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
echo [3/4] Building all plugins...
call tools\build_all.bat
if errorlevel 1 (
    echo.
    echo ERROR: Build failed.
    exit /b 1
)

REM Step 4: Deploy all plugins to debug installation
echo.
echo [4/4] Deploying plugins...
if not exist "debug\plugins" mkdir "debug\plugins"

for /d %%I in (release\plugins\*) do (
    echo   Deploying %%~nI
    if exist "debug\plugins\%%~nI" rmdir /S /Q "debug\plugins\%%~nI"
    robocopy "release\plugins\%%~nI" "debug\plugins\%%~nI" /E /NFL /NDL /NJH /NJS /NC /NS /NP >NUL
)

REM Launch Mod Organizer
echo.
echo Launching Mod Organizer...
start "" "debug\ModOrganizer.exe"

echo.
echo ============================================================================
echo Debug session started.
echo ============================================================================

exit /b 0
