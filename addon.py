import sys
import urllib
import urlparse
import xbmcgui
import xbmcplugin
import CommonFunctions
import re
import time
common = CommonFunctions
common.plugin = "DramaFever-0.1"

#<video class="akamai-html5 akamai-video">
#For DramaFever videos

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

xbmcplugin.setContent(addon_handle, 'movies')

#The current view we are in
#Front Menu = The First View
#Browse = Browse
#Movies = Movies
#Kids = Kids
currentView = 'Front Menu'

#Creates A Video Item
#VideoName: The Name Of The Video
#URL: The URL To The Video
#Icon: The Icon To Display For The Thumbnail
def videoItem(VideoName, URL, Icon):
    foldername = args['foldername'][0]
    videoName = VideoName
    url = URL
    li = xbmcgui.ListItem(label=videoName, iconImage=Icon)
    li.setInfo(type = "Video", infoLabels = {"Title": 'Some Show Title!', "Plot":  'Oooohh Dat Plot Doe', "Year": 'Some Year!'})
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
    xbmcplugin.endOfDirectory(addon_handle)

#Creates A Folder Item
#mode: The Mode(Almost Always Folder)
#foldername: The Name Of the Folder
#iconImage: The Icon To Display For The Thumbnail
def folderItem(mode, foldername, iconImage):
    url = build_url({'mode': mode, 'foldername': foldername})
    print "Folder Item URL Is ----->" + url + "<-----"
    li = xbmcgui.ListItem(foldername, iconImage=iconImage)
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
    currentView = foldername


#shorter version of videoItem
def shorterVideoItem(URL, Icon, overrideLabel):
    if(overrideLabel is ""):
        videoItem(getVideoName(URL), getVideoURL(URL), Icon)
    else:
        videoItem(overrideLabel, getVideoURL(URL), Icon)


#gets the web pages title
#URL: The Web Pages url
def getVideoName(URL):
    htmlStr = urllib.urlopen(URL).read()
    result = common.parseDOM(htmlStr, "div", attrs={"class": "video-title pull-left"})
    #Scrub it and clean it!
    cleanResult = common.stripTags(result[0])
    return repr(cleanResult)


#Gets the videos URL
#URL: The Video pages URL
def getVideoURL(URL):
    return "URLS ARE WHAT I HATE!!!"


def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

mode = args.get('mode', None)

if mode is None:
    #Front View
    currentView = 'Front Menu'
    folderItem('folder', 'Browse', 'DefaultFolder.png')
    folderItem('folder', 'Movies', 'DefaultFolder.png')
    folderItem('folder', 'Kids', 'DefaultFolder.png')
    xbmcplugin.endOfDirectory(addon_handle)
#'https://dramafever-i.akamaihd.net/i/138561/region1/98306efcbd5cc_,5075566,5802847,5828633,5847473,.mp4.csmil/master.m3u8?hdnea=st=1419200128~exp=1419200728~acl=/i/138561/region1/98306efcbd5cc_*~hmac=c4e36a39cbd69de0bf0072ad409c12a99afad273f70e67913d74d88e29b71cbe'
elif mode[0] == 'folder':
    print currentView
    if(currentView == 'Browse'):
        #Browse
        shorterVideoItem('http://www.dramafever.com/drama/3970/1/Running_Man/index.html', 'DefaultFolder.png', 'Browsing Movies/Shows!')
    elif(currentView == 'Movies'):
        #Movies
        shorterVideoItem('http://www.dramafever.com/drama/3970/1/Running_Man/index.html', 'DefaultFolder.png', 'Movies Movies/Shows!')
    elif(currentView == 'Kids'):
        #Kids
        shorterVideoItem('http://www.dramafever.com/drama/3970/1/Running_Man/index.html', 'DefaultFolder.png', 'Kids Movies/Shows!')
