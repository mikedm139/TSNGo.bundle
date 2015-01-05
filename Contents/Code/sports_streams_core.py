import re, urlparse, string, socket, sys, datetime
from dateutil import parser
from dateutil import tz

###############################################
VIDEO_PREFIX = "/video/hockey"
NAME = "Hockey"

ART = 'art-default.png'
ICON = 'icon-default.png'
DEFAULT_TEAM_ICON = "Team_DEFAULT.jpg"

SCHEDULE_URL = "http://smb.cdnak.neulion.com/fs1/nhl/league/schedule/{year}/{month}/{day}/iphone/schedule.json"
GAME_URL = "http://smb.cdnak.neulion.com/fs/nhl/mobile/feed_new/data/streams/2013/ipad/{t}_{gn}.json"

STREAM_AVAILABLE_MINUTES_BEFORE = 20
STREAM_HIDDEN_AFTER = 360 # 6 hours oughta be plenty...
MAIN_MENU_EXTRA_DAYS = 3 # day count not including today and tomorrow
DATE_FORMAT = "%Y-%m-%d"

HERE = tz.tzlocal()
UTC = tz.tzutc()
EASTERN = tz.gettz("EST5EDT")


TEAMS = {
	"ANA": { "City": "Anaheim", "Name": "Ducks", "Logo": "Team_ANA.jpg", "LiveName":"ducks" },
	"BOS": { "City": "Boston", "Name": "Bruins", "Logo": "Team_BOS.jpg", "LiveName":"bruins" },
	"BUF": { "City": "Buffalo", "Name": "Sabres", "Logo": "Team_BUF.jpg", "LiveName":"sabres" },
	"CAR": { "City": "Carolina", "Name": "Hurricanes", "Logo": "Team_CAR.jpg", "LiveName":"hurricanes" },
	"CBJ": { "City": "Columbus", "Name": "Blue Jackets", "Logo": "Team_CBS.jpg", "LiveName":"bluejackets" },
	"CGY": { "City": "Calgary", "Name": "Flames", "Logo": "Team_CGY.jpg", "LiveName":"flames" },
	"CHI": { "City": "Chicago", "Name": "Blackhawks", "Logo": "Team_CHI.jpg", "LiveName":"blackhawks" },
	"COL": { "City": "Colorado", "Name": "Avalanche", "Logo": "Team_COL.jpg", "LiveName":"avalanche" },
	"DAL": { "City": "Dallas", "Name": "Stars", "Logo": "Team_DAL.jpg", "LiveName":"stars" },
	"DET": { "City": "Detroit", "Name": "Red Wings", "Logo": "Team_DET.jpg", "LiveName":"redwings" },
	"EDM": { "City": "Edmonton", "Name": "Oilers", "Logo": "Team_EDM.jpg", "LiveName":"oilers" },
	"FLA": { "City": "Florida", "Name": "Panthers", "Logo": "Team_FLA.jpg", "LiveName":"panthers" },
	"LAK": { "City": "Los Angeles", "Name": "Kings", "Logo": "Team_LOS.jpg", "LiveName":"kings" },
	"MIN": { "City": "Minnesota", "Name": "Wild", "Logo": "Team_MIN.jpg", "LiveName":"wild" },
	"MTL": { "City": "Montreal", "Name": "Canadiens", "Logo": "Team_MON.jpg", "LiveName":"canadiens" },
	"NJD": { "City": "New Jersey", "Name": "Devils", "Logo": "Team_NJD.jpg", "LiveName":"devils" },
	"NSH": { "City": "Nashville", "Name": "Predators", "Logo": "Team_NSH.jpg", "LiveName":"predators" },
	"NYI": { "City": "NY", "Name": "Islanders", "Logo": "Team_NYI.jpg", "LiveName":"islanders" },
	"NYR": { "City": "NY", "Name": "Rangers", "Logo": "Team_NYR.jpg", "LiveName":"rangers" },
	"OTT": { "City": "Ottawa", "Name": "Senators", "Logo": "Team_OTT.jpg", "LiveName":"senators" },
	"PHI": { "City": "Philadelphia", "Name": "Flyers", "Logo": "Team_PHI.jpg", "LiveName":"flyers" },
	"PHX": { "City": "Phoenix", "Name": "Coyotes", "Logo": "Team_PHX.jpg", "LiveName":"coyotes" },
	"PIT": { "City": "Pittsburgh", "Name": "Penguins", "Logo": "Team_PIT.jpg", "LiveName":"penguins" },
	"SJS": { "City": "San Jose", "Name": "Sharks", "Logo": "Team_SAN.jpg", "LiveName":"sharks" },
	"STL": { "City": "St. Louis", "Name": "Blues", "Logo": "Team_STL.jpg", "LiveName":"blues" },
	"TBL": { "City": "Tampa Bay", "Name": "Lightning", "Logo": "Team_TAM.jpg", "LiveName":"lightning" },
	"TOR": { "City": "Toronto", "Name": "Maple Leafs", "Logo": "Team_TOR.jpg", "LiveName":"mapleleafs" },
	"VAN": { "City": "Vancouver", "Name": "Canucks", "Logo": "Team_VAN.jpg", "LiveName":"canucks" },
	"WPG": { "City": "Winnipeg", "Name": "Jets", "Logo": "Team_WPG.jpg", "LiveName":"jets" },
	"WSH": { "City": "Washington", "Name": "Capitals", "Logo": "Team_WSH.jpg", "LiveName":"capitals" }
}

###############################################	

class NotAvailableException(Exception):
	pass
	
	Minutes = STREAM_AVAILABLE_MINUTES_BEFORE
	
class NoGamesException(Exception):
	pass
	

class Game:
	def __init__(self, id, seasonId, type, gameNumber, utcStart, summary, home, away): # pbp
		self.Id = id
		self.SeasonId = seasonId
		self.Type = type
		self.GameNumber = gameNumber
		self.UtcStart = utcStart
		self.Summary = summary
		self.Home = home
		self.Away = away
				
class Team:
	def __init__(self, ab, record, live, replayShort, replayFull):
		self.AB = ab
		self.Record = record
		self.Live = live
		self.ReplayShort = replayShort
		self.ReplayFull = replayFull
		
class GameSummary:
	def __init__(self, id, utcStart, summary, home, away): # pbp
		self.Id = id
		self.UtcStart = utcStart
		self.Summary = summary
		self.Home = home
		self.Away = away
		
class Stream:
	def __init__(self, title, url, team, available, summary):
		self.Title = title
		self.Url = url
		self.Team = team
		self.Available = available
		self.Summary = summary
	
###############################################	

def BuildMainMenu(container, scheduleCallback, archiveCallback):	
	# log some details about the request	
	Log.Info("Hostname: " + str(socket.gethostname()))
	Log.Info("Python Version: " + str(sys.version))
	Log.Info("Platform: " + str(sys.platform))
	Log.Info("Client: " + str(Client.Platform))
	

	# make sure these times, which are used to make calls to the nhl servers, are always in eastern time.
	todayDate = GetToday()
	tomorrowDate = todayDate + datetime.timedelta(days = 1)
	yesterdayDate = todayDate - datetime.timedelta(days = 1)
	
	today = datetime.datetime.strftime(todayDate, DATE_FORMAT)
	tomorrow = datetime.datetime.strftime(tomorrowDate, DATE_FORMAT)
	yesterday = datetime.datetime.strftime(yesterdayDate, DATE_FORMAT)
	
	#yesterday is temporary
	container.add(DirectoryObject(title = "Yesterday", thumb = R(DEFAULT_TEAM_ICON), key = Callback(scheduleCallback, date = yesterday, title = "Yesterday")))
	container.add(DirectoryObject(title = L("TodayLabel"), thumb = R(DEFAULT_TEAM_ICON), key = Callback(scheduleCallback, date = today, title = L("TodayLabel"))))
	container.add(DirectoryObject(title = L("TomorrowLabel"), thumb = R(DEFAULT_TEAM_ICON), key = Callback(scheduleCallback, date = tomorrow, title = L("TomorrowLabel"))))
	
	dateFormat = str(L("ScheduleDateFormat")) # strftime can't take a localstring for some reason.	
	for x in range(1, MAIN_MENU_EXTRA_DAYS + 1):
		date = tomorrowDate + datetime.timedelta(days = x)
		dateString = datetime.datetime.strftime(date, DATE_FORMAT)
		Log.Debug("Main menu date string: " + dateString)
		title = datetime.datetime.strftime(date, dateFormat)
		container.add(DirectoryObject(title = title, thumb = R(DEFAULT_TEAM_ICON), key = Callback(scheduleCallback, date = dateString, title = title)))
		
	#archive
	archiveStartDate = yesterdayDate + datetime.timedelta(days = -8) # the week prior to yesterday
	archiveStartString = datetime.datetime.strftime(archiveStartDate, DATE_FORMAT)
	container.add(DirectoryObject(title=L("ArchiveLabel"), thumb = R(DEFAULT_TEAM_ICON), key = Callback(archiveCallback, startDate = archiveStartString)))
	
def BuildArchiveMenu(container, startDate, scheduleCallBack, archiveCallBack, mainMenuCallBack):
	 
	firstDate = parser.parse(startDate)
	dateFormat = str(L("ScheduleDateFormat")) # strftime can't take a localstring for some reason.	
	
	# earlier games
	earlierDate = firstDate + datetime.timedelta(days = -7)
	earlierDateString = datetime.datetime.strftime(earlierDate, DATE_FORMAT)
	container.add(DirectoryObject(title=L("Earlier"), thumb = R(DEFAULT_TEAM_ICON), key = Callback(archiveCallBack, startDate = earlierDateString)))
	
	for x in range(1, 1 + 7):
		date = firstDate + datetime.timedelta(days = x)
		dateString = datetime.datetime.strftime(date, DATE_FORMAT)
		title = datetime.datetime.strftime(date, dateFormat)
		Log.Debug("Main menu date string: " + dateString)
		container.add(DirectoryObject(title = title, thumb = R(DEFAULT_TEAM_ICON), key = Callback(scheduleCallBack, date = dateString, title = title)))
			
	# later games
	laterDate = firstDate + datetime.timedelta(days = 7)
	laterDateString = datetime.datetime.strftime(laterDate, DATE_FORMAT)
	container.add(DirectoryObject(title=L("Later"), thumb = R(DEFAULT_TEAM_ICON), key = Callback(archiveCallBack, startDate = laterDateString)))
	
	#back to main menu
	container.add(DirectoryObject(title=L("Menu Menu"), thumb = R(DEFAULT_TEAM_ICON), key = Callback(mainMenuCallBack)))
	
	
def BuildScheduleMenu(container, date, gameCallback, mainMenuCallback):
	# get games
	games = GetGameSummariesForDay(date)
	
	if len(games) == 0:
		# no games
		raise NoGamesException
		
	matchupFormat = GetStreamFormatString("MatchupFormat")
	summaryFormat = GetStreamFormatString("SummaryFormat")

	for game in games:
		title = GetStreamFormat(matchupFormat, game.Away, game.Home, game.UtcStart, game.Summary) 
		summary = GetStreamFormat(summaryFormat, game.Away, game.Home, game.UtcStart, game.Summary)
		container.add(DirectoryObject(
			key = Callback(gameCallback, gameId = game.Id, title = title, home=game.Home, away=game.Away, summary=game.Summary),
			title = title,
			summary = summary,
			thumb = R(DEFAULT_TEAM_ICON) 
		))

		
def BuildGameMenu(container, gameId, highlightsCallback, home, away, summary, gameMenuCallback):
	
	game, gameUrl = GetGameAndUrl(gameId)
	
	foundLive = False
	foundReplay = False
		
	# live streams hang around for a while after the game is over.  don't render them if it's over.
	if game["finish"] == "false":
		if "live" in game["gameStreams"]["ipad"]["away"]:
			vco = GetStreamObject(gameUrl, away, "liveAway", "AwayStreamLabelFormat", summary)
			container.add(vco)
			foundLive = True
			
		if "live" in game["gameStreams"]["ipad"]["home"]:
			vco = GetStreamObject(gameUrl, home, "liveHome", "HomeStreamLabelFormat", summary)
			container.add(vco)
			foundLive = True
		
		if foundLive == False:
			title = L("ErrorNotStarted")
			container.add(DirectoryObject(
				key = Callback(gameMenuCallback, gameId=gameId, title=title), # call back to itself makes it go nowhere - in some clients anyway.
				title = title
			))	
			
		
	if game["finish"] == "true":
		#replays away
		if "vod-condensed" in game["gameStreams"]["ipad"]["away"]:
			vco = GetStreamObject(gameUrl, away, "replayShortAway", "AwayReplayCondensedFormat", summary)
			container.add(vco)			
			foundReplay = True
		if "vod-whole" in game["gameStreams"]["ipad"]["away"]:
			vco = GetStreamObject(gameUrl, away, "replayFullAway", "AwayReplayFullFormat", summary)
			container.add(vco)
			foundReplay = True
			
		#replays home
		if "vod-condensed" in game["gameStreams"]["ipad"]["home"]:
			vco = GetStreamObject(gameUrl, home, "replayShortHome", "HomeReplayCondensedFormat", summary)
			container.add(vco)			
			foundReplay = True
		if "vod-whole" in game["gameStreams"]["ipad"]["home"]:
			vco = GetStreamObject(gameUrl, home, "replayFullHome", "HomeReplayFullFormat", summary)
			container.add(vco)
			foundReplay = True
			
		if foundReplay == False:
			title = L("ErrorCompleteNoReplays")
			container.add(DirectoryObject(
				key = Callback(gameMenuCallback, gameId=gameId, title=title), # call back to itself makes it go nowhere - in some clients anyway.
				title = title
			))	
			

def GetStreamObject(gameUrl, teamAbbr, type, labelFormat, summary):
	team = GetTeamConfig(teamAbbr)
	url = gameUrl + "?type=" + type + "&name=" + team["LiveName"] + "&logo=" + team["Logo"] + "&summary=" + summary
	title = str(L(labelFormat)).replace("{name}", team["Name"])
	Log.Debug("stream url: " +  url)
	
	return VideoClipObject(url = url, title = title, thumb = R(team["Logo"]))
	
	

def BuildHighlightsMenu(container, gameId, forHomeTeam, title, selectQualityCallback):

	game, url = GetGameAndUrl(gameId)
	
	url = url + "?type=highlight&home=" + str(forHomeTeam)
	
	for item in game["pbp"]: 
		highlightTitle = item["summary"]
		highlightUrl = url + "&key=" + item["key"] + "&summary=" + highlightTitle + "&logo=" + DEFAULT_TEAM_ICON + "&q=" #append in next menu
		Log.Debug("Highlight json-url: " + highlightUrl)
		container.add(DirectoryObject(
			key = Callback(selectQualityCallback, url = highlightUrl, title = title, logo = DEFAULT_TEAM_ICON, available = True, isHighlight=True),
			title = highlightTitle,
			thumb = R(DEFAULT_TEAM_ICON)
		))
	
	#q = 1600, 800

def BuildQualitySelectionMenu(container, url, logo, isHighlight):
	
	#highlights only have 800 and 1600 available
	if not isHighlight:
		container.add(VideoClipObject(url = url + "4500", title = "4500", thumb = R(logo)))
		container.add(VideoClipObject(url = url + "3000", title = "3000", thumb = R(logo)))
		
	container.add(VideoClipObject(url = url + "1600", title = "1600", thumb = R(logo)))
	
	if not isHighlight:
		container.add(VideoClipObject(url = url + "1200", title = "1200", thumb = R(logo)))
	
	container.add(VideoClipObject(url = url + "800", title = "800", thumb = R(logo)))
	
	if not isHighlight:
		container.add(VideoClipObject(url = url + "400", title = "400", thumb = R(logo)))


def GetStreamDirectory(selectQualityCallback, gameUrl, type, teamAb, titleFormat, available):
	#STREAM_FORMAT = "http://nlds{server}.cdnak.neulion.com/nlds/nhl/{streamName}/as/live/{streamName}_hd_{q}.m3u8"
	team = GetTeamConfig(teamAb)
	Log.Debug("Add clip for " + team["City"])
	
	url = gameUrl + "?type=" + type + "&name=" + team["LiveName"] + "&logo=" + team["Logo"] + "&q=" #appended in next menu
	title = str(titleFormat).replace("{name}", team["Name"])
	
	return DirectoryObject(
		key = Callback(selectQualityCallback, url = url, title = title, logo = team["Logo"], available = available, isHighlight=False),
		title = title,
		thumb = R(team["Logo"])
	)


def GetGameAndUrl(gameId):
	
	t = str(gameId)[4:6]
	gn = str(gameId)[6:]

	url = GAME_URL.replace("{t}", t).replace("{gn}", gn)
	Log.Debug("Loading game from url: " + url)
	game = JSON.ObjectFromURL(url)
	
	
	
	return game, url
	
def GetToday():
	
	#now = datetime.now()
	#hereNow = now.replace(tzinfo=HERE)
	
	today = datetime.datetime.now(EASTERN)
	Log.Debug("Today: " + str(today))
	
	return today
	
def GetGameSummariesForDay(date):
	
	Log.Info("Get games for " + date)
	
	split = date.split("-")
	year = split[0]
	month = split[1]
	day = split[2]
	
	url = SCHEDULE_URL.replace("{year}", year).replace("{month}", month).replace("{day}", day)
	Log.Info("Schedule URL: " + url)
	
	games = []
	
	#try:
	schedule = JSON.ObjectFromURL(url)	
	#except:
	#	Log.Error("Unable to open schedule url")
		# couldn't load url, return no games
	#	return games
	
	Log.Info("Found " + str(len(schedule["games"])) + " games")	
		
	for item in schedule["games"]:		
		gameId = item["gameId"]
		Log.Info("Date: " + date + " " + item["startTime"])
		naive = parser.parse(date + " " + item["startTime"])
		easternStart = naive.replace(tzinfo=EASTERN)
		summary = "" # gamePreview won't exist if game is in progress
		if "gamePreview" in item:
			summary = item["gamePreview"]
		home = item["h"]["ab"]
		away = item["a"]["ab"]
				
		Log.Debug(away + " at " + home + " at " + str(easternStart) + "(ET)")		
		
		game = GameSummary(gameId, easternStart, summary, home, away)		
		games.append(game) 
		
	return games

def GetTeamFromJson(json):
	ab = json["ab"]
	record = json["record"]
	live = json["live"]
	replayShort = json["replayShort"]
	replayFull = json["replayFull"]
	
	return Team(ab, record, live, replayShort, replayFull)

	
def GetStreamFormatString(key):
	CLIENT_OS = (Client.Platform if Client.Platform is not None else "Unknown")
	
	format = L(key + CLIENT_OS)
	if str(format) == key + CLIENT_OS:
		# No client specific MatchupFormat, fallback to default
		format = L(key)
		
	return format
	

def GetStreamFormat(format, awayTeam, homeTeam, utcStart, summary):
	#Log.Debug("utcStart: " + str(utcStart))
	localStart = utcStart.astimezone(HERE).strftime("%H:%M")
	#Log.Debug("localStart: " + str(localStart))
	
	#away = CONFIG.Teams[awayTeam]["City"] + " " + CONFIG.Teams[awayTeam]["Name"]
	#home = CONFIG.Teams[homeTeam]["City"] + " " + CONFIG.Teams[homeTeam]["Name"]
	away = FormatTeamName(awayTeam)
	home = FormatTeamName(homeTeam)
	
	return str(format).replace("{away}", away).replace("{home}", home).replace("{time}", localStart).replace("{summary}", summary)
	
def GetTeamConfig(team):
	if team in TEAMS:
		return TEAMS[team]
	else:
		# create a new team so it's null safe 
		Log.Info("Could not find team configuration for '" + team + "'")
		return { "City": team, "Name": team, "Logo": DEFAULT_TEAM_ICON}
		
def FormatTeamName(team):
	teamConfig = GetTeamConfig(team)
	
	if teamConfig["City"] == teamConfig["Name"]:
		return teamConfig["City"]
	else:
		return teamConfig["City"] + " " + teamConfig["Name"]
	

def GetMinutesToStart(utcStart):
	#Python's date handling is horrifically bad.
	gameStart = utcStart.replace(tzinfo = None) - datetime.datetime.utcnow()
	# to get a logical representation of how long in the future or past the game was, I have to do all this ridiculous math...
	minutesToStart = ((gameStart.microseconds + (gameStart.seconds + gameStart.days * 24 * 3600) * 10**6) / 10.0**6) / 60
	
	return minutesToStart
	
	
