import mobase
from ..base.base_settings import BaseSettings
try:
    from PyQt5.QtCore import qInfo, qDebug, qWarning, qCritical
except:
    from PyQt6.QtCore import qInfo, qDebug, qWarning, qCritical

class CommonLog():
    """Class handling logging functions for Mod Organizer plugins."""

    def __init__(self, plugin:str, organiser:mobase.IOrganizer, settings:BaseSettings):
        self._organiser = organiser
        self._plugin = plugin
        self._settings = settings

    def _prefix(self):
        return "[" + self._plugin + "] "

    def debug(self, message:str):
        if self._settings.loglevel() < 1:
            qDebug(self._prefix() + message)

    def info(self, message:str):
        if self._settings.loglevel() < 2:
            qInfo(self._prefix() + message)

    def warning(self, message:str):
        if self._settings.loglevel() < 3:
            qWarning(self._prefix() + message)

    def critical(self, message:str):
        if self._settings.loglevel() < 4:
            qCritical(self._prefix() + message) 
