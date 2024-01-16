from .plugin.shortcutter.plugins.shortcutter_manager import ShortcutterManager

def createPlugins():
    return [
        ShortcutterManager()
    ]