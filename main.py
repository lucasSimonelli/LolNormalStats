import requests
from lxml import html
#Finds a substring between 2 given phrases
def find_between( s, first, last ):
	try:
		start = s.index( first ) + len( first )
		end = s.index( last, start )
		return s[start:end]
	except ValueError:
		return ""

#Harcoded to lolking html structure
def getStatus(match):
	if match.get('class')=='match_win':
		return True
	return False

#Harcoded to lolking html structure
def getChampionName(detail):
	return detail[0][0][0][0].get('href')[11:]

r = requests.get("http://www.lolking.net/summoner/las/235830")

historyHTML = find_between(r.text,"<!-- MATCH HISTORY -->","<!-- MASTERIES -->")
historyHTML = historyHTML.rstrip('\n')[3:-2] #Removing \n hardcodily.
parsed = html.fromstring(historyHTML)

for match in parsed:
	won = getStatus(match)
	for detail in match:
		#ignoring extended details for now
		if detail.get('class')=='match_details_extended':
			continue

		#1st cell: champion
		champion = getChampionName(detail)

		#2nd cell: game type
		gameType = detail[1][0][0].text

		#3rd cell: duration <ignored>

		#4th cell: kda
		kills = detail[3][0][0].text
		deaths = detail[3][0][3].text
		assists = detail[3][0][6].text
		
		#4th cell: gold
		gold = float(detail[4][0][0].text[0:-1])*1000

		#5th cell: minions
		minions = detail[5][0][0].text
		
"""for post in parsed:
    for child in post:
        print child.text

for post in parsed:
    print post.text"""