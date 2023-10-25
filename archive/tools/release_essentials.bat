@echo off
cd /D "%~dp0\..\"

echo Removing existing release folder.
rmdir /S /Q "release\essentials"

echo Creating release folder.
mkdir "release\essentials"

robocopy "src\curationclub" "release\essentials\curationclub" /E
robocopy "src\essentials" "release\essentials\essentials" /E
robocopy "src\pluginfinder" "release\essentials\pluginfinder" /E
robocopy "directory" "release\essentials\pluginfinder" "plugin_directory.json"
robocopy "src\profilesync" "release\essentials\profilesync" /E
robocopy "src\reinstaller" "release\essentials\reinstaller" /E
robocopy "src\rootbuilder" "release\essentials\rootbuilder" /E
robocopy "src\shared" "release\essentials\shared" /E
robocopy "src\shortcutter" "release\essentials\shortcutter" /E
robocopy "src" "release\essentials" "__init__.py"

cd /D "%~dp0\..\release" 
tar.exe -a -cf "zip\essentials.zip" "essentials" 
