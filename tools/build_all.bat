@echo off
setlocal enabledelayedexpansion

REM ============================================================================
REM build_all.bat - Build all plugins using their current versions
REM
REM Usage: build_all.bat
REM
REM This script builds all plugins in src\plugin\ without changing versions.
REM ============================================================================

REM Get script directory and change to repo root
set "SCRIPT_DIR=%~dp0"
cd /D "%SCRIPT_DIR%.."

echo.
echo ============================================================================
echo                     Building All Plugins
echo ============================================================================

REM Discover all plugins
set "PLUGIN_LIST="
for /d %%I in (src\plugin\*) do (
    set "PLUGIN_LIST=!PLUGIN_LIST! %%~nI"
)

if "%PLUGIN_LIST%"=="" (
    echo ERROR: No plugins found in src\plugin\
    exit /b 1
)

REM Clean plugins folder
echo.
echo Cleaning release\plugins directory...
if exist "release\plugins" (
    rmdir /S /Q "release\plugins"
)
mkdir "release\plugins"

REM Build all plugins
call tools\build.bat %PLUGIN_LIST%

exit /b %ERRORLEVEL%
