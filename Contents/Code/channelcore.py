import re, urlparse, string, socket, sys, datetime, locale
from dateutil import tz
from dateutil import parser
import urllib2
import urllib
import __init__ as channel



def Init():
	# Initialize the plugin
	Plugin.AddPrefixHandler(channel.VIDEO_PREFIX, MainMenu, channel.NAME, channel.ICON, channel.ART)
	Plugin.AddViewGroup("List", viewMode = "InfoList", mediaType = "items")

	ObjectContainer.title1 = channel.NAME
	
	Log.Debug("Plugin Start")
	

def LogMainMenu():	
	Log.Info("Hostname: " + str(socket.gethostname()))
	Log.Info("Python Version: " + str(sys.version))
	Log.Info("Platform: " + str(sys.platform))
	Log.Info("Client: " + str(Client.Platform))
	

def MainMenu():	
		
	# log some details about the request
	LogMainMenu()
	
	dir = ObjectContainer(title2 = channel.NAME, art=R(channel.ART), view_group = "List")
				
	for channelItem in channel.CHANNEL_LIST:
		channelData = JSON.ObjectFromURL(channelItem)
		
		Log.Debug("Found Channel: " + channelItem)
		
		name = channelData["name"]
		logo_key = channelData["logo_key"]
		schedule = channelData["schedule"]
		currentlyPlaying = ""
		nextUp = ""
		nextUpTime = None
		
		if schedule != "":		
			currentlyPlaying, nextUp, nextUpTime = channel.GetScheduledShows(channelData["schedule"])		
	
		if currentlyPlaying == "":
			currentlyPlaying = name
			
		# Format: 1:05 PM
		summary = ""
		if nextUpTime != None:
			summary = "Up Next: " + nextUp + " @ " + nextUpTime.strftime("%I:%M %p").lstrip("0")
		
		url = channelItem + "?desc=" + urllib.quote(currentlyPlaying)
				
		dir.add(VideoClipObject(
						url = url,
						summary = summary,
						title = currentlyPlaying,
						thumb = R(logo_key)
					))
	return dir

def GetNowPlaying(nowPlayingUrl):
	try:
		nowPlayingData = JSON.ObjectFromURL(nowPlayingUrl)
		description = nowPlayingData["value"]["items"][0]["Name"]
		return description
	except:
		return ""
	