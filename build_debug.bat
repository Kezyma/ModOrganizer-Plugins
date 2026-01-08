@echo off
setlocal enabledelayedexpansion

REM ============================================================================
REM build_debug.bat - Build debug versions of all plugins
REM
REM Usage: build_debug.bat [nopause]
REM   nopause: Optional flag to skip the pause at the end (for automation)
REM
REM This script:
REM   1. Processes ALL plugins in the repository
REM   2. For each plugin:
REM      - Increments Z version (x.y.Z -> x.y.Z+1)
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
echo                     ModOrganizer-Plugins Debug Builder
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

echo Found %PLUGIN_COUNT% plugins to build.
echo.

REM Create a reusable PowerShell script for version extraction (avoids batch escaping issues)
set "GET_VER_SCRIPT=%TEMP%\mo2_get_version_%RANDOM%.ps1"
powershell -NoProfile -Command "Set-Content -Path '%GET_VER_SCRIPT%' -Value 'param($file); $c = Get-Content $file -Raw; if ($c -match ''mobase\.VersionInfo\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)'') { Write-Output \"$($matches[1]).$($matches[2]).$($matches[3])\" } else { Write-Output ''0.0.0'' }'"

REM Clean only the plugins folder (leave zip files alone)
echo Cleaning release\plugins directory...
if exist "release\plugins" (
    rmdir /S /Q "release\plugins"
)
mkdir "release\plugins"
echo.

REM Build all plugins
echo ============================================================================
echo Starting Debug Build
echo ============================================================================

set "BUILD_COUNT=0"
set "FAILED_COUNT=0"

for /L %%i in (1,1,%PLUGIN_COUNT%) do (
    set "PNAME=!PLUGIN_%%i!"
    set "PFILE=src\plugin\!PNAME!\core\!PNAME!_plugin.py"

    REM Get current version using the pre-created PowerShell script
    for /f "delims=" %%v in ('powershell -NoProfile -ExecutionPolicy Bypass -File "!GET_VER_SCRIPT!" "!PFILE!"') do (
        set "CURRENT_VER=%%v"
    )

    REM Parse current version and calculate new version
    for /f "tokens=1,2,3 delims=." %%a in ("!CURRENT_VER!") do (
        set "VX=%%a"
        set "VY=%%b"
        set "VZ=%%c"
    )

    REM Increment Z
    set /a "NEW_Z=!VZ!+1"
    set "NEW_VERSION=!VX!.!VY!.!NEW_Z!"

    echo.
    echo [%%i/%PLUGIN_COUNT%] Building !PNAME!: !CURRENT_VER! -^> !NEW_VERSION!

    REM Call build.bat
    call build.bat "!PNAME!" "!NEW_VERSION!"

    if errorlevel 1 (
        set /a FAILED_COUNT+=1
        echo FAILED: !PNAME!
    ) else (
        set /a BUILD_COUNT+=1
    )
)

echo.
echo ============================================================================
echo Debug Build Complete
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
