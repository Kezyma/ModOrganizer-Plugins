@echo off
cd /D "%~dp0\..\"

echo Removing existing release folder.
rmdir /S /Q "release"