from ..shortcutter.plugins.shortcutter_tool_create import ShortcutterCreateTool
import mobase

class ShortcutterEssentials(ShortcutterCreateTool):

    def __init__(self):
        super().__init__()

    def init(self, organiser=mobase.IOrganizer):
        return super().init(organiser)

    def displayName(self):
        return "Essentials/" + self.baseDisplayName()