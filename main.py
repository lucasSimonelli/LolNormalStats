import requests
from lxml import html
from models import *
import Tkinter as tk

constants={}
constants['normal']="Normal 5v5"
constants['aram']="Howling Abyss"
constants['rankedTeam']="Ranked Team 5v5"
constants['soloQ']="Ranked Solo 5v5"
constants['lolkingUrl'] = "http://www.lolking.net/summoner/las/235830"
constants['startTrim'] = "<!-- MATCH HISTORY -->"
constants['endTrim'] = "<!-- MASTERIES -->"
constants['detailsExtended'] = 'match_details_extended'
constants['dataGameIdClass'] = 'data-game-id'
constants['winText'] = "Win" 
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


def updateDatabase():
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
				updateGameTypeSpecificStats(dbObject)
				session.add(dbObject)

	session.commit()

def updateGameTypeSpecificStats(dbObject):
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


def computeChampionKDA():
	pass

setup_all()
create_all()
updateDatabase()

class ExampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        t = SimpleTable(self, 10,2)
        t.pack(side="top", fill="x")
        t.set(0,0,"Hello, world")

class SimpleTable(tk.Frame):
    def __init__(self, parent, rows=10, columns=2):
        # use black background so it "peeks through" to 
        # form grid lines
        tk.Frame.__init__(self, parent, background="black")
        self._widgets = []
        for row in range(rows):
            current_row = []
            for column in range(columns):
                label = tk.Label(self, text="%s/%s" % (row, column), 
                                 borderwidth=0, width=10)
                label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                current_row.append(label)
            self._widgets.append(current_row)

        for column in range(columns):
            self.grid_columnconfigure(column, weight=1)


    def set(self, row, column, value):
        widget = self._widgets[row][column]
        widget.configure(text=value)

if __name__ == "__main__":
    app = ExampleApp()
    app.mainloop()