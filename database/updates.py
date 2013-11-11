from utilities.constants import constants
from database.models import *
def updateGameTypeSpecificStats(dbObject, gameType):
	if gameType == constants['normal']:
		updateNormalStats(dbObject)
	elif gameType == constants['aram']:
		updateAramStats(dbObject)
	elif gameType == constants['rankedTeam']:
		updateRankedTeamStats(dbObject)
	elif gameType == constants['soloQ']:
		updateSoloQStats(dbObject)

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
