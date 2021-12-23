import mobase
from pathlib import Path
from .essentials.rootbuilder_mapper import RootBuilderMapperEssentials
from .essentials.rootbuilder import RootBuilderEssentials
from .essentials.reinstaller import ReinstallerEssentials
from .essentials.shortcutter import ShortcutterEssentials
from .essentials.pluginfinder import PluginFinderEssentials
from .essentials.curationclub import CurationClubEssentials
from .essentials.profilesync import ProfileSyncEssentials

def createPlugins():
    plugins = []
    pluginDir = Path(__file__).parent.parent

    rbInit = pluginDir / "rootbuilder" / "__init__.py"
    if not rbInit.exists():
        plugins.append(RootBuilderEssentials())
        plugins.append(RootBuilderMapperEssentials())

    riInit = pluginDir / "reinstaller" / "__init__.py"
    if not riInit.exists():
        plugins.append(ReinstallerEssentials())

    scInit = pluginDir / "shortcutter" / "__init__.py"
    if not scInit.exists():
        plugins.append(ShortcutterEssentials())

    pfInit = pluginDir / "pluginfinder" / "__init__.py"
    if not pfInit.exists():
        plugins.append(PluginFinderEssentials())

    ccInit = pluginDir / "curationclub" / "__init__.py"
    if not ccInit.exists():
        plugins.append(CurationClubEssentials())

    psInit = pluginDir / "profilesync" / "__init__.py"
    if not psInit.exists():
        plugins.append(ProfileSyncEssentials())

    return plugins

