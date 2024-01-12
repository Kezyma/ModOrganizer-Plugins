from .plugin.listexporter.plugins.listexplorer_htmlexport import ListExplorerHtmlExport
from .plugin.listexporter.plugins.listexplorer_jsonexport import ListExplorerJsonExport

def createPlugins():
    return [
        ListExplorerHtmlExport(),
        ListExplorerJsonExport()
    ]