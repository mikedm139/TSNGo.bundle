import live_core as live


###############################################

VIDEO_PREFIX = "/video/tsn"
NAME = "TSN"

LISTINGS_URL = "https://rawgit.com/pudds/JsonData/master/tv/tsn.json"

ART = 'art-default.png'
ICON = 'icon-default.png'
ICON_LIVETV = 'tsn-channels.jpg'


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
	live.LogMainMenu()
	
	dir.add(DirectoryObject(title = L("Live TV"), thumb = R(ICON_LIVETV), key = Callback(LiveTVMenu)))
	
	return dir
	
def LiveTVMenu():

	dir = ObjectContainer(title2 = L("Live TV"), art=R(ICON_LIVETV), view_group = "List")
	
	live.BuildChannelMenu(dir, LISTINGS_URL, LiveTVChannel)
			
	return dir
	 	
def LiveTVChannel(name, url, logo):
	
	dir = ObjectContainer(title2 = name, art=logo)
	
	baseurl = url + "?title=" + name + "&logo=" + logo
	#baseurl = LIVETV_FORMAT.replace("{server}", server).replace("{title}", title).replace("{logo}", icon).replace("{channel}", channel)
	
	url8 = baseurl.replace("{quality}", "8")
	url7 = baseurl.replace("{quality}", "7")
	url6 = baseurl.replace("{quality}", "6")
	url5 = baseurl.replace("{quality}", "5")
	url4 = baseurl.replace("{quality}", "4")
	url3 = baseurl.replace("{quality}", "3")
	url2 = baseurl.replace("{quality}", "2")
	url1 = baseurl.replace("{quality}", "1")
	
	dir.add(VideoClipObject(url = url8, title = "Quality 8", thumb = logo))
	dir.add(VideoClipObject(url = url7, title = "Quality 7", thumb = logo))
	dir.add(VideoClipObject(url = url6, title = "Quality 6", thumb = logo))
	dir.add(VideoClipObject(url = url5, title = "Quality 5", thumb = logo))
	dir.add(VideoClipObject(url = url4, title = "Quality 4", thumb = logo))
	dir.add(VideoClipObject(url = url3, title = "Quality 3", thumb = logo))
	dir.add(VideoClipObject(url = url2, title = "Quality 2", thumb = logo))
	dir.add(VideoClipObject(url = url1, title = "Quality 1", thumb = logo))
	
	
	return dir
	
####################################
# supplemental functions

def GetToday():
		
	today = datetime.datetime.now(EASTERN)
	Log.Debug("Today: " + str(today))
	
	return today