@echo off

:: arg 1 = Shortcut Name
:: arg 2 = Shortcut Path
:: arg 3 = Icon Path
:: arg 4 = Arguments

:: Get desktop location
setlocal EnableExtensions DisableDelayedExpansion
set "DesktopFolder="
for /F "skip=1 tokens=1,2*" %%I in ('%SystemRoot%\System32\reg.exe QUERY "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders" /v Desktop 2^>nul') do if /I "%%I" == "Desktop" if not "%%~K" == "" if "%%J" == "REG_SZ" (set "DesktopFolder=%%~K") else if "%%J" == "REG_EXPAND_SZ" call set "DesktopFolder=%%~K"
if not defined DesktopFolder for /F "skip=1 tokens=1,2*" %%I in ('%SystemRoot%\System32\reg.exe QUERY "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders" /v Desktop 2^>nul') do if /I "%%I" == "Desktop" if not "%%~K" == "" if "%%J" == "REG_SZ" (set "DesktopFolder=%%~K") else if "%%J" == "REG_EXPAND_SZ" call set "DesktopFolder=%%~K"
if not defined DesktopFolder set "DesktopFolder=\"
if "%DesktopFolder:~-1%" == "\" set "DesktopFolder=%DesktopFolder:~0,-1%"
if not defined DesktopFolder set "DesktopFolder=%UserProfile%\Desktop"

:: Generate shortcut
echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo sLinkFile = "%DesktopFolder%\" + %1 + ".lnk" >> CreateShortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs
echo oLink.TargetPath = %2 >> CreateShortcut.vbs
echo oLink.Arguments = %4 >> CreateShortcut.vbs
echo oLink.Description = %1 >> CreateShortcut.vbs
echo oLink.IconLocation = %3 >> CreateShortcut.vbs
echo oLink.Save >> CreateShortcut.vbs
cscript CreateShortcut.vbs
del CreateShortcut.vbs


