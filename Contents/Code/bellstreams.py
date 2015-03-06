import re, urlparse, string, socket, sys, datetime, locale
from dateutil import tz
from dateutil import parser
import urllib2
import urllib
	
HERE = tz.tzlocal()
UTC = tz.tzutc()
EASTERN = tz.gettz("EST5EDT")
	
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