from utilities.constants import constants
from database.models import *

def getNormalStats(champion):
	query = NormalStats.query.filter_by(champion=champion)
	if not query.count():
		return None
	return query.first()

def getSoloQStats(champion):
	query = SoloQStats.query.filter_by(champion=champion)
	if not query.count():
		return None
	return query.first()

def getAramStats(champion):
	query = AramStats.query.filter_by(champion=champion)
	if not query.count():
		return None
	return query.first()

def getCustomStats(champion):
	query = CustomStats.query.filter_by(champion=champion)
	if not query.count():
		return None
	return query.first()

def getTeamRankedStats(champion):
	query = RankedTeamStats.query.filter_by(champion=champion)
	if not query.count():
		return None
	return query.first()

#Classy pythonic "switch" statement
options = {
	constants['normal']:getNormalStats,
	constants['soloQ']:getSoloQStats,
	constants['aram']:getAramStats,
	constants['rankedTeam']:getTeamRankedStats,
	constants['custom']:getCustomStats,
}

#Returns a dict with the query results
def getChampionStats(champion, gameType):
	query = options[gameType](champion)
	if query == None:
		return None
	return query.to_dict()