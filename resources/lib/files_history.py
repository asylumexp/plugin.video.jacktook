import os
from resources.lib.db.database import get_db
from resources.lib.utils.kodi import ADDON_PATH
from xbmcgui import ListItem
from xbmcplugin import (
    addDirectoryItem,
    endOfDirectory,
    setPluginCategory,
)


def last_files(plugin, func1, func2):
    setPluginCategory(plugin.handle, f"Last Files - History")

    list_item = ListItem(label="Clear Files")
    list_item.setArt(
        {"icon": os.path.join(ADDON_PATH, "resources", "img", "clear.png")}
    )
    addDirectoryItem(
        plugin.handle,
        plugin.url_for(func1, type="lfh"),
        list_item,
    )

    for title, data in reversed(get_db().database["jt:lfh"].items()):
        formatted_time = data["timestamp"].strftime("%a, %d %b %Y %I:%M %p")
        label = f"{title}—{formatted_time}"
        list_item = ListItem(label=label)
        list_item.setArt(
            {"icon": os.path.join(ADDON_PATH, "resources", "img", "magnet.png")}
        )
        list_item.setProperty("IsPlayable", "true")
        addDirectoryItem(
            plugin.handle,
            plugin.url_for(
                func2,
                query=f"{data.get('url', None)} {data.get('magnet', None)} {data.get('id')} {title}",
            ),
            list_item,
            False,
        )
    endOfDirectory(plugin.handle)
