import re, urlparse, string, socket, sys, datetime, locale
from dateutil import tz


###############################################



SPORT_KEYWORD = "hockey"
LIVETV_FORMAT = "http://ams-lp{server}.9c9media.com/hls-live/livepkgr/_definst_/liveeventNoDRM/{channel}Open{quality}.m3u8?title={title}&logo={logo}"

VIDEO_PREFIX = "/video/tsn"
NAME = "TSN"

ART = 'art-default.png'
ICON = 'icon-default.png'
ICON_LIVETV = 'tsn-channels.jpg'
ICON_TSN1 = 'tsn1.png'
ICON_TSN2 = 'tsn2.png'
ICON_TSN3 = 'tsn3.png'
ICON_TSN4 = 'tsn4.png'
ICON_TSN5 = 'tsn5.png'

HERE = tz.tzlocal()
UTC = tz.tzutc()
EASTERN = tz.gettz("EST5EDT")

###############################################

# This function is initially called by PMS to inialize the plugin

def Start():

	# Initialize the plugin
	Plugin.AddPrefixHandler(VIDEO_PREFIX, MainMenu, NAME, ICON, ART)
	Plugin.AddViewGroup("List", viewMode = "InfoList", mediaType = "items")

	ObjectContainer.title1 = NAME
	
	Log.Debug("Plugin Start")

def MainMenu():
	dir = ObjectContainer(title2 = L("MainMenuTitle"), art=R(ART), view_group = "List")
	
	# log some details about the request	
	Log.Info("Hostname: " + str(socket.gethostname()))
	Log.Info("Python Version: " + str(sys.version))
	Log.Info("Platform: " + str(sys.platform))
	Log.Info("Client: " + str(Client.Platform))
	
	dir.add(DirectoryObject(title = L("Live TV"), thumb = R(ICON_LIVETV), key = Callback(LiveTVMenu)))
	
	return dir
	
def LiveTVMenu():

	dir = ObjectContainer(title2 = L("Live TV"), art=R(ICON_LIVETV), view_group = "List")
	
	dir.add(DirectoryObject(title = "TSN1", thumb = R(ICON_TSN1), key = Callback(LiveTVChannel, title = "TSN1", icon = ICON_TSN1)))
	dir.add(DirectoryObject(title = "TSN2", thumb = R(ICON_TSN2), key = Callback(LiveTVChannel, title = "TSN2", icon = ICON_TSN2)))
	dir.add(DirectoryObject(title = "TSN3", thumb = R(ICON_TSN3), key = Callback(LiveTVChannel, title = "TSN3", icon = ICON_TSN3)))
	dir.add(DirectoryObject(title = "TSN4", thumb = R(ICON_TSN4), key = Callback(LiveTVChannel, title = "TSN4", icon = ICON_TSN4)))
	dir.add(DirectoryObject(title = "TSN5", thumb = R(ICON_TSN5), key = Callback(LiveTVChannel, title = "TSN5", icon = ICON_TSN5)))
	
	return dir
	 	
def LiveTVChannel(title, icon):
	
	dir = ObjectContainer(title2 = title, art=R(icon))
	
	server = ""
	channel = ""
		
	if title == "TSN1":
		server = "5"
		channel = "tsn"
	elif title == "TSN2":
		server = "7"
		channel = "TSN2"		
	elif title == "TSN3":
		server = "1"
		channel = "TSN3"
	elif title == "TSN4":
		server = "2"
		channel = "TSN4"
	elif title == "TSN5":
		server = "3"
		channel = "TSN5"
		
		
	baseurl = LIVETV_FORMAT.replace("{server}", server).replace("{title}", title).replace("{logo}", icon).replace("{channel}", channel)
	
	url8 = baseurl.replace("{quality}", "8")
	url7 = baseurl.replace("{quality}", "7")
	url6 = baseurl.replace("{quality}", "6")
	url5 = baseurl.replace("{quality}", "5")
	url4 = baseurl.replace("{quality}", "4")
	url3 = baseurl.replace("{quality}", "3")
	url2 = baseurl.replace("{quality}", "2")
	url1 = baseurl.replace("{quality}", "1")
	
	dir.add(VideoClipObject(url = url8, title = "Quality 8", thumb = R(icon)))
	dir.add(VideoClipObject(url = url7, title = "Quality 7", thumb = R(icon)))
	dir.add(VideoClipObject(url = url6, title = "Quality 6", thumb = R(icon)))
	dir.add(VideoClipObject(url = url5, title = "Quality 5", thumb = R(icon)))
	dir.add(VideoClipObject(url = url4, title = "Quality 4", thumb = R(icon)))
	dir.add(VideoClipObject(url = url3, title = "Quality 3", thumb = R(icon)))
	dir.add(VideoClipObject(url = url2, title = "Quality 2", thumb = R(icon)))
	dir.add(VideoClipObject(url = url1, title = "Quality 1", thumb = R(icon)))
	
	
	return dir
	
	