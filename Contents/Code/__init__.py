import datetime
from dateutil import tz
from dateutil import parser
import channelcore as core
import bellstreams


###############################################

VIDEO_PREFIX = "/video/tsngo"
NAME = "TSN Go"

ART = 'art-default.jpg'
ICON = 'icon-default.png'

CHANNEL_LIST = [
	'https://raw.githubusercontent.com/pudds/JsonData/master/channels/tsn/tsn.json',
	'https://raw.githubusercontent.com/pudds/JsonData/master/channels/tsn/tsn2.json',
	'https://raw.githubusercontent.com/pudds/JsonData/master/channels/tsn/tsn3.json',
	'https://raw.githubusercontent.com/pudds/JsonData/master/channels/tsn/tsn4.json',
	'https://raw.githubusercontent.com/pudds/JsonData/master/channels/tsn/tsn5.json'
	]

###############################################

# This function is initially called by PMS to inialize the plugin
def Start():
	core.Init()

def GetScheduledShows(scheduleUrl):
	return bellstreams.GetScheduledShows(scheduleUrl)