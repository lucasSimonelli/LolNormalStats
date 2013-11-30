from utilities.constants import constants
from database.models import *

def getChampionStats(champion, gameType):
	query = Match.query.filter_by(champion=champion, gameType= gameType)
	if not query.count():
		return None
	return query
