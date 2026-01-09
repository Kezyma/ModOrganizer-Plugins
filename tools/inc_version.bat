@echo off
setlocal enabledelayedexpansion

REM ============================================================================
REM inc_version.bat - Increment minor version (Y) and reset build (Z) to 0
REM
REM Usage: inc_version.bat [plugin1] [plugin2] ...
REM        inc_version.bat all
REM        inc_version.bat              (interactive mode)
REM
REM Version format: x.y.z
REM   x = major (unchanged)
REM   y = minor (incremented)
REM   z = build (reset to 0)
REM
REM Example: 1.2.5 -> 1.3.0
REM ============================================================================

REM Get script directory and change to repo root
set "SCRIPT_DIR=%~dp0"
cd /D "%SCRIPT_DIR%.."

REM Create temporary PowerShell script for version extraction
set "PS_SCRIPT=%TEMP%\mo2_get_ver_%RANDOM%.ps1"
echo param($file) > "%PS_SCRIPT%"
echo $c = Get-Content $file -Raw >> "%PS_SCRIPT%"
echo if ($c -match 'mobase\.VersionInfo\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)') { >> "%PS_SCRIPT%"
echo     Write-Output "$($matches[1]).$($matches[2]).$($matches[3])" >> "%PS_SCRIPT%"
echo } else { Write-Output '0.0.0' } >> "%PS_SCRIPT%"

REM Handle "all" argument
if /i "%~1"=="all" (
    set "PLUGINS_TO_UPDATE="
    for /d %%I in (src\plugin\*) do (
        set "PLUGINS_TO_UPDATE=!PLUGINS_TO_UPDATE! %%~nI"
    )
    goto :do_update
)

REM If arguments provided, use them
if not "%~1"=="" (
    set "PLUGINS_TO_UPDATE=%*"
    goto :do_update
)

REM Interactive mode - no arguments provided
echo.
echo ============================================================================
echo                     Increment Minor Version (Y)
echo                     Example: 1.2.5 -^> 1.3.0
echo ============================================================================

REM Discover all plugins and show with current versions
set "PLUGIN_COUNT=0"
for /d %%I in (src\plugin\*) do (
    set /a PLUGIN_COUNT+=1
    set "PLUGIN_!PLUGIN_COUNT!=%%~nI"
)

if %PLUGIN_COUNT%==0 (
    echo ERROR: No plugins found in src\plugin\
    del "%PS_SCRIPT%" 2>nul
    exit /b 1
)

echo.
echo Available plugins:
echo.
for /L %%i in (1,1,%PLUGIN_COUNT%) do (
    set "PNAME=!PLUGIN_%%i!"
    set "PFILE=src\plugin\!PNAME!\core\!PNAME!_plugin.py"

    for /f "delims=" %%v in ('powershell -NoProfile -ExecutionPolicy Bypass -File "%PS_SCRIPT%" "!PFILE!"') do (
        set "VER_%%i=%%v"
    )

    echo   [%%i] !PNAME! ^(v!VER_%%i!^)
)

echo.
echo   [A] Update ALL plugins
echo   [0] Cancel
echo.

set /p "SELECTION=Enter plugin numbers separated by spaces (e.g., 1 3 5) or A for all: "

if /i "%SELECTION%"=="0" (
    echo Cancelled.
    del "%PS_SCRIPT%" 2>nul
    exit /b 0
)

REM Parse selection
set "PLUGINS_TO_UPDATE="
if /i "%SELECTION%"=="A" (
    for /L %%i in (1,1,%PLUGIN_COUNT%) do (
        set "PLUGINS_TO_UPDATE=!PLUGINS_TO_UPDATE! !PLUGIN_%%i!"
    )
) else (
    for %%i in (%SELECTION%) do (
        set "VALID=0"
        for /L %%j in (1,1,%PLUGIN_COUNT%) do (
            if "%%i"=="%%j" (
                set "VALID=1"
                set "PLUGINS_TO_UPDATE=!PLUGINS_TO_UPDATE! !PLUGIN_%%j!"
            )
        )
        if "!VALID!"=="0" (
            echo WARNING: Invalid selection '%%i', skipping.
        )
    )
)

if "%PLUGINS_TO_UPDATE%"=="" (
    echo No valid plugins selected.
    del "%PS_SCRIPT%" 2>nul
    exit /b 1
)

:do_update
echo.
echo ============================================================================
echo                     Incrementing Minor Version
echo ============================================================================

set "UPDATE_COUNT=0"
set "FAILED_COUNT=0"

for %%P in (%PLUGINS_TO_UPDATE%) do (
    set "PLUGIN_NAME=%%P"
    set "PLUGIN_FILE=src\plugin\!PLUGIN_NAME!\core\!PLUGIN_NAME!_plugin.py"

    if not exist "!PLUGIN_FILE!" (
        echo ERROR: Plugin file not found: !PLUGIN_FILE!
        set /a FAILED_COUNT+=1
    ) else (
        REM Get current version
        for /f "delims=" %%v in ('powershell -NoProfile -ExecutionPolicy Bypass -File "%PS_SCRIPT%" "!PLUGIN_FILE!"') do (
            set "OLD_VER=%%v"
        )

        REM Parse and calculate new version
        for /f "tokens=1,2,3 delims=." %%a in ("!OLD_VER!") do (
            set "VX=%%a"
            set "VY=%%b"
            set "VZ=%%c"
        )

        set /a "NEW_Y=!VY!+1"
        set "NEW_VER=!VX!.!NEW_Y!.0"

        REM Update the file
        powershell -NoProfile -ExecutionPolicy Bypass -Command "$f='!PLUGIN_FILE!'; $c=Get-Content $f -Raw; $c=$c -replace 'mobase\.VersionInfo\s*\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*(,\s*\d+\s*)?\)','mobase.VersionInfo(!VX!, !NEW_Y!, 0)'; Set-Content $f -Value $c -NoNewline"

        if errorlevel 1 (
            echo ERROR: Failed to update !PLUGIN_NAME!
            set /a FAILED_COUNT+=1
        ) else (
            echo !PLUGIN_NAME!: !OLD_VER! -^> !NEW_VER!
            set /a UPDATE_COUNT+=1
        )
    )
)

REM Cleanup
del "%PS_SCRIPT%" 2>nul

echo.
echo ============================================================================
echo Version Update Summary: %UPDATE_COUNT% updated, %FAILED_COUNT% failed
echo ============================================================================

if %FAILED_COUNT% GTR 0 exit /b 1
exit /b 0
