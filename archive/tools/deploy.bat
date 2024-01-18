@echo off
cd /D "%~dp0"

echo Looping through mods.
for %%x in (%*) do (
	echo Deploying %%x
	for /F "tokens=*" %%A in (deploy_targets.txt) do (
		echo Deploying to %%A
		rmdir /S /Q "%%A\%%x"
		mkdir "%%A\%%x"
		robocopy "..\release\%%x" "%%A\%%x" /E
	)
)
