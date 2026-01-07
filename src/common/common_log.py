from ..base.base_settings import BaseSettings
try:
    from PyQt5.QtCore import qInfo, qDebug, qWarning, qCritical
except:
    from PyQt6.QtCore import qInfo, qDebug, qWarning, qCritical

class CommonLog:
    """Class handling logging functions for Mod Organizer plugins."""

    def __init__(self, plugin: str, settings: BaseSettings) -> None:
        self._prefix = f"[{plugin}] "
        self._settings = settings

    def _get_loglevel(self) -> int:
        """Get loglevel with fallback to 0 (most verbose) if settings not initialized."""
        level = self._settings.loglevel()
        return level if level is not None else 0

    def debug(self, message: str) -> None:
        if self._get_loglevel() < 1:
            qDebug(f"{self._prefix}{message}")

    def info(self, message: str) -> None:
        if self._get_loglevel() < 2:
            qInfo(f"{self._prefix}{message}")

    def warning(self, message: str) -> None:
        if self._get_loglevel() < 3:
            qWarning(f"{self._prefix}{message}")

    def critical(self, message: str) -> None:
        if self._get_loglevel() < 4:
            qCritical(f"{self._prefix}{message}") 
