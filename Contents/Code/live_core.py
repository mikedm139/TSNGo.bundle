import re, urlparse, string, socket, sys, datetime, locale
from dateutil import tz
from dateutil import parser
import urllib2
import urllib
import __init__ as channel




def LogMainMenu():	
	Log.Info("Hostname: " + str(socket.gethostname()))
	Log.Info("Python Version: " + str(sys.version))
	Log.Info("Platform: " + str(sys.platform))
	Log.Info("Client: " + str(Client.Platform))
	

def BuildChannelMenu(container, listingsUrl, callback):
	
	lineup = JSON.ObjectFromURL(listingsUrl)
	
	for channelItem in lineup["Channels"]:
		currentlyPlaying, nextUp, nextUpTime = channel.GetScheduledShows(channelItem["Schedule"])
		
		Log.Debug("Found Channel: " + channelItem["Name"] + "; Currently Playing: " + currentlyPlaying)
		
		if currentlyPlaying == "":
			currentlyPlaying = channelItem["Name"]
		
		# Format: 1:05 PM
		summary = ""
		if nextUpTime != None:
			summary = "Up Next: " + nextUp + " @ " + nextUpTime.strftime("%I:%M %p").lstrip("0")
			
		url = channelItem["Feed"] + "?title=" + channelItem["Name"] + "&desc=" + urllib.quote(currentlyPlaying) + "&logo=" + channelItem["Logo"]
		menuItem = VideoClipObject(url = url, title = currentlyPlaying, thumb = channelItem["Logo"], summary = summary)
	
		container.add(menuItem)
		