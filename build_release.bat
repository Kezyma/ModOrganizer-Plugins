@echo off
setlocal enabledelayedexpansion

REM ============================================================================
REM build_release.bat - Build release versions of selected plugins
REM
REM Usage: build_release.bat [nopause]
REM   nopause: Optional flag to skip the pause at the end (for automation)
REM
REM This script:
REM   1. Lists all available plugins
REM   2. Allows user to select which plugins to build
REM   3. For each selected plugin:
REM      - Increments Y version and sets Z to 0 (x.Y.z -> x.Y+1.0)
REM      - Generates UI files
REM      - Creates release package
REM ============================================================================

REM Check for nopause flag
set "NOPAUSE=0"
if /i "%~1"=="nopause" set "NOPAUSE=1"

REM Get script directory
set "SCRIPT_DIR=%~dp0"
cd /D "%SCRIPT_DIR%"

echo.
echo ============================================================================
echo                     ModOrganizer-Plugins Release Builder
echo ============================================================================
echo.

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

REM Create a reusable PowerShell script for version extraction (avoids batch escaping issues)
set "GET_VER_SCRIPT=%TEMP%\mo2_get_version_%RANDOM%.ps1"
powershell -NoProfile -Command "Set-Content -Path '%GET_VER_SCRIPT%' -Value 'param($file); $c = Get-Content $file -Raw; if ($c -match ''mobase\.VersionInfo\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)'') { Write-Output \"$($matches[1]).$($matches[2]).$($matches[3])\" } else { Write-Output ''0.0.0'' }'"

REM Display plugin list with current versions
echo Available plugins:
echo.
for /L %%i in (1,1,%PLUGIN_COUNT%) do (
    set "PNAME=!PLUGIN_%%i!"
    set "PFILE=src\plugin\!PNAME!\core\!PNAME!_plugin.py"

    REM Get current version using the pre-created PowerShell script
    for /f "delims=" %%v in ('powershell -NoProfile -ExecutionPolicy Bypass -File "!GET_VER_SCRIPT!" "!PFILE!"') do (
        set "CURRENT_VER_%%i=%%v"
    )

    echo   [%%i] !PNAME! ^(current: !CURRENT_VER_%%i!^)
)

echo.
echo   [A] Build ALL plugins
echo   [0] Cancel
echo.

REM Get user selection
set /p "SELECTION=Enter plugin numbers separated by spaces (e.g., 1 3 5) or A for all: "

if /i "%SELECTION%"=="0" (
    echo Build cancelled.
    exit /b 0
)

REM Parse selection
set "SELECTED_PLUGINS="
if /i "%SELECTION%"=="A" (
    for /L %%i in (1,1,%PLUGIN_COUNT%) do (
        set "SELECTED_PLUGINS=!SELECTED_PLUGINS! %%i"
    )
) else (
    set "SELECTED_PLUGINS=%SELECTION%"
)

REM Validate and build selected plugins
echo.
echo ============================================================================
echo Starting Release Build
echo ============================================================================

set "BUILD_COUNT=0"
set "FAILED_COUNT=0"

for %%i in (%SELECTED_PLUGINS%) do (
    REM Validate selection is a number in range
    set "VALID=0"
    for /L %%j in (1,1,%PLUGIN_COUNT%) do (
        if "%%i"=="%%j" set "VALID=1"
    )

    if "!VALID!"=="0" (
        echo WARNING: Invalid selection '%%i', skipping.
    ) else (
        set "PNAME=!PLUGIN_%%i!"
        set "CURRENT_VER=!CURRENT_VER_%%i!"

        REM Parse current version and calculate new version
        for /f "tokens=1,2,3 delims=." %%a in ("!CURRENT_VER!") do (
            set "VX=%%a"
            set "VY=%%b"
            set "VZ=%%c"
        )

        REM Increment Y, set Z to 0
        set /a "NEW_Y=!VY!+1"
        set "NEW_VERSION=!VX!.!NEW_Y!.0"

        echo.
        echo Building !PNAME!: !CURRENT_VER! -^> !NEW_VERSION!

        REM Remove existing release folder for this plugin only
        if exist "release\plugins\!PNAME!" (
            rmdir /S /Q "release\plugins\!PNAME!"
        )

        REM Call build.bat
        call build.bat "!PNAME!" "!NEW_VERSION!"

        if errorlevel 1 (
            set /a FAILED_COUNT+=1
            echo FAILED: !PNAME!
        ) else (
            set /a BUILD_COUNT+=1
        )
    )
)

echo.
echo ============================================================================
echo Release Build Complete
echo ============================================================================
echo.
echo   Successful: %BUILD_COUNT%
echo   Failed:     %FAILED_COUNT%
echo.
echo Release files are in: release\
echo Plugin folders are in: release\plugins\
echo.

REM Cleanup temp script
del "%GET_VER_SCRIPT%" 2>nul

if "%NOPAUSE%"=="0" PAUSE

exit /b 0
