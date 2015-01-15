import re, urlparse, string, socket, sys, datetime, locale
from dateutil import tz
from dateutil import parser
import urllib2


HERE = tz.tzlocal()
UTC = tz.tzutc()
EASTERN = tz.gettz("EST5EDT")



def LogMainMenu():	
	Log.Info("Hostname: " + str(socket.gethostname()))
	Log.Info("Python Version: " + str(sys.version))
	Log.Info("Platform: " + str(sys.platform))
	Log.Info("Client: " + str(Client.Platform))
	

def BuildChannelMenu(container, listingsUrl, callback):
	
	lineup = JSON.ObjectFromURL(listingsUrl)
	
	for channel in lineup["Channels"]:
		Log.Debug(channel["Name"])
		currentlyPlaying, nextUp, nextUpTime = GetScheduledShows(channel["Schedule"])
		Log.Debug(currentlyPlaying)
		
		# Format: 1:05 PM
		summary = "Up Next: " + nextUp + " @ " + nextUpTime.strftime("%I:%M %p").lstrip("0")
		
		#channelName = channel["Name"] + " - " + currentlyPlaying
		#menuItem = DirectoryObject(title = currentlyPlaying, thumb = channel["Logo"], summary = summary, key = Callback(callback, name = channel["Name"], url = channel["Feed"], logo = channel["Logo"]))
		# url = url8, title = "Quality 8", thumb = logo		
		url = channel["Feed"] + "?title=" + channel["Name"] + "&desc=" + currentlyPlaying + "&logo=" + channel["Logo"]
		menuItem = VideoClipObject(url = url, title = currentlyPlaying, thumb = channel["Logo"], summary = summary)
	
		container.add(menuItem)
		
def GetScheduledShows(scheduleUrl):
	schedule = JSON.ObjectFromURL(scheduleUrl)
		
	nowEastern = datetime.datetime.now(EASTERN)
	
	nowPlaying = ""
	foundCurrent = False
	upNext = ""
	upNextStart = None
	
	for item in schedule["Items"]:
		startTime = parser.parse(item["StartTime"])
		endTime = parser.parse(item["EndTime"])
		if nowEastern >= startTime and nowEastern < endTime:
			nowPlaying = item["Name"]
			foundCurrent = True
			continue
		if foundCurrent == True:
			# we found the current one, and we're still in the loop, so this must be the next one.
			upNext = item["Name"]
			upNextStart = parser.parse(item["StartTime"]).astimezone(HERE)
			break # we're done here.
			
	#end for
	
	return nowPlaying, upNext, upNextStart