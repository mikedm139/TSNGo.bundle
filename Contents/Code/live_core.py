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
		currentlyPlaying = GetCurrentShow(channel["Schedule"])
		Log.Debug(currentlyPlaying)
		
		#channelName = channel["Name"] + " - " + currentlyPlaying
		menuItem = DirectoryObject(title = currentlyPlaying, thumb = channel["Logo"], key = Callback(callback, name = channel["Name"], url = channel["Feed"], logo = channel["Logo"]))
		container.add(menuItem)
		
def GetCurrentShow(scheduleUrl):
	schedule = JSON.ObjectFromURL(scheduleUrl)
		
	nowEastern = datetime.datetime.now(EASTERN)
	
	for item in schedule["Items"]:
		startTime = parser.parse(item["StartTime"])
		endTime = parser.parse(item["EndTime"])
		if nowEastern >= startTime and nowEastern < endTime:
			return item["Name"]