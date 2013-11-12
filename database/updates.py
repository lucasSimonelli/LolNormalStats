from utilities.constants import constants
from database.models import *
from utilities.inout import loadLolkingHTML

def updateGameTypeSpecificStats(dbObject, gameType):
	if gameType == constants['normal']:
		updateNormalStats(dbObject)
	elif gameType == constants['aram']:
		updateAramStats(dbObject)
	elif gameType == constants['rankedTeam']:
		updateRankedTeamStats(dbObject)
	elif gameType == constants['soloQ']:
		updateSoloQStats(dbObject)
	elif gameType == constants['custom']:
		updateCustomStats(dbObject)

def updateNormalStats(obj):
	query = NormalStats.query.filter_by(champion=obj.champion)
	#If we have no stats for that champion
	if not query.count():
		dbObject = NormalStats(champion=obj.champion,kills=obj.kills,deaths=obj.deaths,assists=obj.assists,gold=obj.gold,minions=obj.minions)
		if obj.won:
			dbObject.wins=1
		else:
			dbObject.losses=1
		session.add(dbObject)
	else:
		stat = query.first()
		updateStat(stat,obj)

def updateAramStats(obj):
	query = AramStats.query.filter_by(champion=obj.champion)
	#If we have no stats for that champion
	if not query.count():
		dbObject = AramStats(champion=obj.champion,kills=obj.kills,deaths=obj.deaths,assists=obj.assists,gold=obj.gold,minions=obj.minions)
		if obj.won:
			dbObject.win+=1
		else:
			dbObject.losses=1
		session.add(dbObject)
	else:
		stat = query.first()
		updateStat(stat,obj)

def updateRankedTeamStats(obj):
	query = RankedTeamStats.query.filter_by(champion=obj.champion)
	#If we have no stats for that champion
	if not query.count():
		dbObject = RankedTeamStats(champion=obj.champion,kills=obj.kills,deaths=obj.deaths,assists=obj.assists,gold=obj.gold,minions=obj.minions)
		if obj.won:
			dbObject.wins=1
		else:
			dbObject.losses=1
		session.add(dbObject)
	else:
		stat = query.first()
		updateStat(stat,obj)

def updateSoloQStats(obj):
	query = SoloQStats.query.filter_by(champion=obj.champion)
	#If we have no stats for that champion
	if not query.count():
		dbObject = SoloQStats(champion=obj.champion,kills=obj.kills,deaths=obj.deaths,assists=obj.assists,gold=obj.gold,minions=obj.minions)
		if obj.won:
			dbObject.wins=1
		else:
			dbObject.losses=1
		session.add(dbObject)
	else:
		stat = query.first()
		updateStat(stat,obj)

def updateCustomStats(obj):
	query = CustomStats.query.filter_by(champion=obj.champion)
	#If we have no stats for that champion
	if not query.count():
		dbObject = CustomStats(champion=obj.champion,kills=obj.kills,deaths=obj.deaths,assists=obj.assists,gold=obj.gold,minions=obj.minions)
		if obj.won:
			dbObject.wins=1
		else:
			dbObject.losses=1
		session.add(dbObject)
	else:
		stat = query.first()
		updateStat(stat,obj)

def updateStat(stat,newObj):
	stat.kills+=newObj.kills
	stat.deaths+=newObj.deaths
	stat.assists+=newObj.assists
	stat.gold+=newObj.gold
	stat.minions+=newObj.minions

	if newObj.won:
		stat.wins+=1
	else:
		stat.losses+=1


#Harcoded to lolking html structure
def getChampionName(detail):
	return detail[0][0][0][0].get('href')[11:]

def matchWasWon(detail):
	if detail[1][0][1].text==constants['winText'] :
		return True
	return False


def extractData(detail,gameID):
	#1st cell: champion
	champion = getChampionName(detail)

	#2nd cell: game type & w/l
	gameType = detail[1][0][0].text

	#2nd cell: game type
	won = matchWasWon(detail)

	#3rd cell: duration <ignored>

	#4th cell: kda
	kills = int(detail[3][0][0].text)
	deaths = int(detail[3][0][3].text)
	assists = int(detail[3][0][6].text)
	
	#4th cell: gold
	gold = int(float(detail[4][0][0].text[0:-1])*1000)

	#5th cell: minions
	minions = int(detail[5][0][0].text)

	dbObject = Match(champion=champion, gameID=gameID, gameType=gameType,won=won,kills=kills,deaths=deaths,assists=assists,gold=gold,minions=minions)
	updateGameTypeSpecificStats(dbObject,gameType)
	session.add(dbObject)


def loadNewMatches(json):
	parsed = loadLolkingHTML(json)
	for match in parsed:
		gameID = int(match.get(constants['dataGameIdClass']))
		#Check if match is already in db
		if not Match.query.filter_by(gameID=gameID).count():
			for detail in match:
				#ignoring extended details for now
				if detail.get('class')==constants['detailsExtended']:
					continue
				extractData(detail,gameID)
	session.commit()