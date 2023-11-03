try:
    from PyQt5.QtGui import QIcon
except:
    from PyQt6.QtGui import QIcon
from pathlib import Path

def icon(icon: str) -> QIcon:
    return QIcon(str(Path(__file__).parent.joinpath("icons").joinpath(icon)))

CHECK_ICON = icon("ui-check.ico")
MENU_ICON = icon("ui-menu.ico")
MINUS_ICON = icon("ui-minus.ico")
PLUS_ICON = icon("ui-plus.ico")
SYNC_ICON = icon("ui-sync.ico")
LINK_ICON = icon("ui-link.ico")
PLUGIN_ICON = icon("ui-plugin.ico")
NEXUS_ICON = icon("ui-nexus.ico")
PATREON_ICON = icon("ui-patreon.ico")
GITHUB_ICON = icon("ui-github.ico")
INSTALL_ICON = icon("ui-install.ico")
DOCS_ICON = icon("ui-docs.ico")
PREV_ICON = icon("ui-prev.ico")
NEXT_ICON = icon("ui-next.ico")
INFO_ICON = icon("ui-info.ico")
WARNING_ICON = icon("ui-warning.ico")
STOP_ICON = icon("ui-stop.ico")
UPDATE_ICON = icon("ui-update.ico")
UPDATE_ALT_ICON = icon("ui-update-alt.ico")
NO_UPDATE_ICON = icon("ui-no-update.ico")
REFRESH_ICON = icon("ui-refresh.ico")
TRASH_ICON = icon("ui-trash.ico")
ALPHA_ICON = icon("ui-alpha.ico")
BETA_ICON = icon("ui-beta.ico")
GAMMA_ICON = icon("ui-gamma.ico")
DELTA_ICON = icon("ui-delta.ico")
DOWNLOAD_ICON = icon("ui-download.ico")
LINK_ALT_ICON = icon("ui-link-alt.ico")
FILTER_ICON = icon("ui-filter.ico")
RECYCLE_ICON = icon("ui-recycle.ico")
OPENMW_ICON = icon("ui-openmw.ico")
CLIP_ICON = icon("ui-clip.ico")
DISCORD_ICON = icon("ui-discord.ico")
