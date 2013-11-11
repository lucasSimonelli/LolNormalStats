from constants import constants
from models import *

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
}

#Returns a dict with the query results
def getChampionStats(champion, gameType):
	query = options[gameType](champion)
	if query == None:
		return None
	return query.to_dict()