#Libs
import requests, tkMessageBox, json
from lxml import html
from Tkinter import *
import ttk
#My packages
from database.queries import getChampionStats
from database.updates import updateGameTypeSpecificStats
from database.models import *
from utilities.constants import constants, champions
from utilities.inout import printHtmlTable
from utilities.misc import findBetween



#Harcoded to lolking html structure
def getChampionName(detail):
	return detail[0][0][0][0].get('href')[11:]

def matchWasWon(detail):
	if detail[1][0][1].text==constants['winText'] :
		return True
	return False

def loadNewMatches(js):
	r = requests.get(js['lolkingUrl'])

	historyHTML = findBetween(r.text,constants['startTrim'],constants['endTrim'])
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
				gold = int(float(detail[4][0][0].text[0:-1])*1000)

				#5th cell: minions
				minions = int(detail[5][0][0].text)

				dbObject = Match(champion=champion, gameID=gameID, gameType=gameType,won=won,kills=kills,deaths=deaths,assists=assists,gold=gold,minions=minions)
				updateGameTypeSpecificStats(dbObject,gameType)
				session.add(dbObject)

	session.commit()

js={}
try:
	config = open('config.json')
	js = json.load(config) 
	config.close()
except IOError:
	js['lolkingUrl'] = constants['lolkingUrl']
	



master = Tk('LolNormalStats')
master.title('LolNormalStats')
w=master.winfo_screenwidth()
h=master.winfo_screenheight()
master.geometry("300x100+%d+%d" % ( (w-300)/2, (h-100)/2 ) )
w = Label(master, text="Your lolking url:")
w.grid(columnspan=2)

e = Entry(master, width=50)
e.insert(0, js['lolkingUrl'])
e.grid(columnspan=2)



e.focus_set()

setup_all()
create_all()
def callback():
	try:
		js['lolkingUrl']=e.get()
		tkMessageBox.showinfo(
			"Ok Url",
			"Url loaded successfully"
		)
	except requests.exceptions.MissingSchema:
		tkMessageBox.showerror(
			"Wrong Url",
			"Cannot open provided url"
		)

def getData():
	try:
		pb1 = ttk.Progressbar(master, mode='determinate', name='pb1')
		loadNewMatches(js)
		tkMessageBox.showinfo(
			"Ok Url",
			"data downloaded successfully"
		)
	except requests.exceptions.MissingSchema:
		tkMessageBox.showerror(
			"Wrong Url",
			"Cannot open provided url"
		)

b = Button(master, text="Load lolking url", command=callback)
b.grid(row=2, column=0)


b2 = Button(master, text="Get data", command=getData)
b2.grid(row=2, column=1)


mainloop()



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
printHtmlTable(l)

config = open('config.json','w')
json.dump(js, config, sort_keys=True, indent=4)
config.close()
print "#Lata!"