import sys

from urllib.parse import urlencode, parse_qsl

import xbmcaddon
import xbmcgui
import xbmcplugin
import xbmc

self = xbmcaddon.Addon()

PLUGIN_URL      = sys.argv[0]
PLUGIN_HANDLE   = int(sys.argv[1])

def main(paramStr):
    params = dict(parse_qsl(paramStr[1:]))

    xbmcplugin.setContent(PLUGIN_HANDLE, "addons")
    xbmcplugin.setPluginCategory(PLUGIN_HANDLE, 'Plugin List')

    if not params:

        for i in range(9):
            listItem = xbmcgui.ListItem(self.getLocalizedString(30001 + i))
            listItem.setArt({'thumb' : self.getAddonInfo('icon'), 'poster': self.getAddonInfo('fanart')})
            listItem.setProperty('IsPlayable', 'false')

            xbmcplugin.addDirectoryItem(PLUGIN_HANDLE, '{}?list={}'.format(PLUGIN_URL, i + 1), listItem, True)

        xbmcplugin.endOfDirectory(PLUGIN_HANDLE)

    elif params.get('list', '') != '':

        pluginList = self.getSettings().getStringList('list{}'.format(params['list']))
        for plugin in pluginList:
            addon = xbmcaddon.Addon(plugin)

            listItem = xbmcgui.ListItem(addon.getAddonInfo('name'))
            listItem.setArt({'thumb' : addon.getAddonInfo('icon'), 'poster': addon.getAddonInfo('fanart')})
            
            infoTag = listItem.getVideoInfoTag()
            #infoTag.setMediaType("video")
            infoTag.setTitle(addon.getAddonInfo('summary'))
            infoTag.setPlot(addon.getAddonInfo('description'))
            #infoTag.setPath(broadcast['url'])

            listItem.setProperty('IsPlayable', 'false')
            xbmcplugin.addDirectoryItem(PLUGIN_HANDLE, '{}?plugin={}'.format(PLUGIN_URL, plugin), listItem, False)

        xbmcplugin.endOfDirectory(PLUGIN_HANDLE)

    elif params.get('plugin', '') != '':

        xbmc.executebuiltin('RunAddon({})'.format(params['plugin']))

if __name__ == '__main__':
    main(sys.argv[2])
