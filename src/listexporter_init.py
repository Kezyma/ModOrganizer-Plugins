from .plugin.listexporter.plugins.listexporter_manager import ListExporterManager


def createPlugins():
    return [
        ListExporterManager()
    ]
