import mobase
from .shortcutter.plugins.shortcutter_tool_create import ShortcutterCreateTool

def createPlugins():
    return [
        ShortcutterCreateTool()
        ]