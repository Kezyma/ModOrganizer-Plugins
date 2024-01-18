@echo off
cd /D "%~dp0\"

echo Clearing logs.
del /F /Q "release_log.txt"
del /F /Q "deploy_log.txt"

cd /D "%~dp0\..\"

echo Removing existing release folder.
rmdir /S /Q "release"