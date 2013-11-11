import requests
from lxml import html
from models import *
import Tkinter as tk
from queries import getChampionStats
from updates import updateGameTypeSpecificStats
from constants import constants, champions
from inout import printHtmlTable


#Finds a substring between 2 given phrases
def find_between( s, first, last ):
	try:
		start = s.index( first ) + len( first )
		end = s.index( last, start )
		return s[start:end]
	except ValueError:
		return ""

#Harcoded to lolking html structure
def getChampionName(detail):
	return detail[0][0][0][0].get('href')[11:]

def matchWasWon(detail):
	if detail[1][0][1].text==constants['winText'] :
		return True
	return False

def loadNewMatches():
	r = requests.get(constants['lolkingUrl'])

	historyHTML = find_between(r.text,constants['startTrim'],constants['endTrim'])
	historyHTML = historyHTML.rstrip('\n')[3:-2] #Removing \n hardcodily.
	parsed = html.fromstring(historyHTML)

	for match in parsed:
		gameID = int(match.get(constants['dataGameIdClass']))
		#Check if match is already in db
		if not Match.query.filter_by(gameID=gameID).count():
			for detail in match:
				#ignoring extended details for now
				if detail.get('class')==constants['detailsExtended']:
					continue
				
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
				gold = float(detail[4][0][0].text[0:-1])*1000

				#5th cell: minions
				minions = int(detail[5][0][0].text)

				dbObject = Match(champion=champion, gameID=gameID, gameType=gameType,won=won,kills=kills,deaths=deaths,assists=assists,gold=gold,minions=minions)
				updateGameTypeSpecificStats(dbObject,gameType)
				session.add(dbObject)

	session.commit()

setup_all()
create_all()
loadNewMatches()

l=[]
firstTime=True
for champion in champions:
	dict=getChampionStats(champion.lower(), constants['normal'])
	if dict==None:
		continue
	if firstTime:
		firstTime=False
		l.append(dict.keys())
	#The html printer doesnt like to print the 0 integer, apparently
	if (dict['wins']==0):
		dict['wins']="0"
	if (dict['losses']==0):
		dict['losses']="0"
	l.append(dict.values())
	print dict.values()
printHtmlTable(l)
