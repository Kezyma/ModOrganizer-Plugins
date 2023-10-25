FOR /R ..\src %%G IN (*.ui) DO (
    python -m PyQt6.uic.pyuic "%%G" -o "%%~dpGqt6\%%~nG.py"
    python -m PyQt5.uic.pyuic "%%G" -o "%%~dpGqt5\%%~nG.py"
)
PAUSE