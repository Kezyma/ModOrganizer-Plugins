@echo off
setlocal enabledelayedexpansion

REM ============================================================================
REM debug.bat - Build specified plugin(s) and launch Mod Organizer for testing
REM
REM Usage: debug.bat [plugin1] [plugin2] ...
REM        debug.bat all
REM        debug.bat              (interactive mode)
REM
REM This script:
REM   1. Stops any running Mod Organizer instance
REM   2. Downloads and installs MO2 v2.5.2 if not present
REM   3. Builds the specified plugin(s)
REM   4. Deploys built plugins to debug\plugins\
REM   5. Launches Mod Organizer
REM ============================================================================

REM Get script directory and change to repo root
set "SCRIPT_DIR=%~dp0"
cd /D "%SCRIPT_DIR%.."

REM Handle "all" argument
if /i "%~1"=="all" (
    call tools\debug_all.bat
    exit /b %ERRORLEVEL%
)

REM If arguments provided, use them directly
if not "%~1"=="" (
    set "PLUGINS_TO_BUILD=%*"
    goto :do_debug
)

REM Interactive mode - no arguments provided
echo.
echo ============================================================================
echo                     Debug Plugins
echo ============================================================================

REM Discover all plugins
set "PLUGIN_COUNT=0"
for /d %%I in (src\plugin\*) do (
    set /a PLUGIN_COUNT+=1
    set "PLUGIN_!PLUGIN_COUNT!=%%~nI"
)

if %PLUGIN_COUNT%==0 (
    echo ERROR: No plugins found in src\plugin\
    exit /b 1
)

echo.
echo Available plugins:
echo.
for /L %%i in (1,1,%PLUGIN_COUNT%) do (
    echo   [%%i] !PLUGIN_%%i!
)

echo.
echo   [A] Debug ALL plugins
echo   [0] Cancel
echo.

set /p "SELECTION=Enter plugin numbers separated by spaces (e.g., 1 3 5) or A for all: "

if /i "%SELECTION%"=="0" (
    echo Cancelled.
    exit /b 0
)

REM Parse selection
set "PLUGINS_TO_BUILD="
if /i "%SELECTION%"=="A" (
    call tools\debug_all.bat
    exit /b %ERRORLEVEL%
) else (
    for %%i in (%SELECTION%) do (
        set "VALID=0"
        for /L %%j in (1,1,%PLUGIN_COUNT%) do (
            if "%%i"=="%%j" (
                set "VALID=1"
                set "PLUGINS_TO_BUILD=!PLUGINS_TO_BUILD! !PLUGIN_%%j!"
            )
        )
        if "!VALID!"=="0" (
            echo WARNING: Invalid selection '%%i', skipping.
        )
    )
)

if "%PLUGINS_TO_BUILD%"=="" (
    echo No valid plugins selected.
    exit /b 1
)

:do_debug
echo.
echo ============================================================================
echo                     Debug Runner
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

REM Step 3: Build plugins
echo.
echo [3/4] Building plugins...
call tools\build.bat %PLUGINS_TO_BUILD%
if errorlevel 1 (
    echo.
    echo ERROR: Build failed.
    exit /b 1
)

REM Step 4: Deploy plugins to debug installation
echo.
echo [4/4] Deploying plugins...
if not exist "debug\plugins" mkdir "debug\plugins"

for %%P in (%PLUGINS_TO_BUILD%) do (
    if exist "release\plugins\%%P" (
        echo   Deploying %%P
        if exist "debug\plugins\%%P" rmdir /S /Q "debug\plugins\%%P"
        robocopy "release\plugins\%%P" "debug\plugins\%%P" /E /NFL /NDL /NJH /NJS /NC /NS /NP >NUL
    )
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
