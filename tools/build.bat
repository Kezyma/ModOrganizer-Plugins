@echo off
setlocal enabledelayedexpansion

REM ============================================================================
REM build.bat - Build specified plugin(s) using their current version
REM
REM Usage: build.bat [plugin1] [plugin2] ...
REM        build.bat all
REM        build.bat              (interactive mode)
REM
REM This script:
REM   1. For each specified plugin:
REM      - Reads current version from plugin file
REM      - Generates UI files for PyQt5 and PyQt6
REM      - Copies plugin files to release\plugins\<plugin_name>
REM      - Creates a versioned zip file at release\<plugin_name>\<plugin_name>.<version>.zip
REM ============================================================================

REM Get script directory and change to repo root
set "SCRIPT_DIR=%~dp0"
cd /D "%SCRIPT_DIR%.."

REM Handle "all" argument
if /i "%~1"=="all" (
    call tools\build_all.bat
    exit /b %ERRORLEVEL%
)

REM If arguments provided, use them directly
if not "%~1"=="" (
    set "PLUGINS_TO_BUILD=%*"
    goto :do_build
)

REM Interactive mode - no arguments provided
echo.
echo ============================================================================
echo                     Build Plugins
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
echo   [A] Build ALL plugins
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
    call tools\build_all.bat
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

:do_build
REM Create PowerShell script for version extraction (3-digit: x.y.z)
set "PS_SCRIPT=%TEMP%\mo2_get_ver_%RANDOM%.ps1"
echo param($file) > "%PS_SCRIPT%"
echo $c = Get-Content $file -Raw >> "%PS_SCRIPT%"
echo if ($c -match 'mobase\.VersionInfo\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)') { >> "%PS_SCRIPT%"
echo     Write-Output "$($matches[1]).$($matches[2]).$($matches[3])" >> "%PS_SCRIPT%"
echo } else { Write-Output '0.0.0' } >> "%PS_SCRIPT%"

REM Process each plugin
set "BUILD_COUNT=0"
set "FAILED_COUNT=0"

for %%P in (%PLUGINS_TO_BUILD%) do (
    set "PLUGIN_NAME=%%P"

    REM Check if plugin exists
    if not exist "src\plugin\!PLUGIN_NAME!" (
        echo ERROR: Plugin '!PLUGIN_NAME!' not found in src\plugin\
        set /a FAILED_COUNT+=1
    ) else (
        REM Get current version
        set "PLUGIN_FILE=src\plugin\!PLUGIN_NAME!\core\!PLUGIN_NAME!_plugin.py"
        for /f "delims=" %%v in ('powershell -NoProfile -ExecutionPolicy Bypass -File "%PS_SCRIPT%" "!PLUGIN_FILE!"') do (
            set "VERSION=%%v"
        )

        echo.
        echo ============================================================================
        echo Building !PLUGIN_NAME! v!VERSION!
        echo ============================================================================

        REM Step 1: Generate UI files
        echo [1/3] Generating UI files...
        set "UI_DIR=src\plugin\!PLUGIN_NAME!\ui"

        if exist "!UI_DIR!" (
            for /R "!UI_DIR!" %%G in (*.ui) do (
                echo   Processing %%~nxG

                if not exist "%%~dpGqt5" mkdir "%%~dpGqt5"
                if not exist "%%~dpGqt6" mkdir "%%~dpGqt6"

                python -m PyQt6.uic.pyuic "%%G" -o "%%~dpGqt6\%%~nG.py" 2>nul
                python -m PyQt5.uic.pyuic "%%G" -o "%%~dpGqt5\%%~nG.py" 2>nul
            )
        ) else (
            echo   No UI directory found, skipping.
        )

        REM Step 2: Copy files to release directory
        echo [2/3] Copying files to release\plugins\!PLUGIN_NAME!...

        if not exist "release\plugins" mkdir "release\plugins"

        if exist "release\plugins\!PLUGIN_NAME!" (
            rmdir /S /Q "release\plugins\!PLUGIN_NAME!"
        )
        mkdir "release\plugins\!PLUGIN_NAME!"

        robocopy "src\plugin\!PLUGIN_NAME!" "release\plugins\!PLUGIN_NAME!\plugin\!PLUGIN_NAME!" /E /NFL /NDL /NJH /NJS /NC /NS /NP >nul
        robocopy "src\base" "release\plugins\!PLUGIN_NAME!\base" /E /NFL /NDL /NJH /NJS /NC /NS /NP >nul
        robocopy "src\common" "release\plugins\!PLUGIN_NAME!\common" /E /NFL /NDL /NJH /NJS /NC /NS /NP >nul

        if exist "src\!PLUGIN_NAME!_init.py" (
            copy "src\!PLUGIN_NAME!_init.py" "release\plugins\!PLUGIN_NAME!\__init__.py" >nul
        ) else (
            echo   WARNING: Init file not found: src\!PLUGIN_NAME!_init.py
        )

        REM Step 3: Create zip file
        echo [3/3] Creating release\!PLUGIN_NAME!\!PLUGIN_NAME!.!VERSION!.zip...

        if not exist "release\!PLUGIN_NAME!" mkdir "release\!PLUGIN_NAME!"

        if exist "release\!PLUGIN_NAME!\!PLUGIN_NAME!.!VERSION!.zip" (
            del "release\!PLUGIN_NAME!\!PLUGIN_NAME!.!VERSION!.zip"
        )

        cd "release\plugins"
        tar.exe -a -cf "..\!PLUGIN_NAME!\!PLUGIN_NAME!.!VERSION!.zip" "!PLUGIN_NAME!" 2>nul
        cd "%SCRIPT_DIR%.."

        if exist "release\!PLUGIN_NAME!\!PLUGIN_NAME!.!VERSION!.zip" (
            echo Build complete: !PLUGIN_NAME! v!VERSION!
            set /a BUILD_COUNT+=1
        ) else (
            echo ERROR: Failed to create zip file.
            set /a FAILED_COUNT+=1
        )
    )
)

REM Cleanup
del "%PS_SCRIPT%" 2>nul

echo.
echo ============================================================================
echo Build Summary: %BUILD_COUNT% successful, %FAILED_COUNT% failed
echo ============================================================================

if %FAILED_COUNT% GTR 0 exit /b 1
exit /b 0
