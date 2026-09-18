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

    def _format(self, message: str) -> str:
        """Prefixes a message and makes it safe for Qt's logging functions.

        Qt's logging takes a C string, which PyQt encodes as ascii, so a mod name,
        profile name or file path containing accented, Cyrillic or CJK characters
        would otherwise raise UnicodeEncodeError inside whatever operation happened
        to be logging at the time. Escaping keeps those characters identifiable.
        """
        return f"{self._prefix}{message}".encode("ascii", errors="backslashreplace").decode("ascii")

    def debug(self, message: str) -> None:
        if self._get_loglevel() < 1:
            qDebug(self._format(message))

    def info(self, message: str) -> None:
        if self._get_loglevel() < 2:
            qInfo(self._format(message))

    def warning(self, message: str) -> None:
        if self._get_loglevel() < 3:
            qWarning(self._format(message))

    def critical(self, message: str) -> None:
        if self._get_loglevel() < 4:
            qCritical(self._format(message))
