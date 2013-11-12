#Libs
import tkMessageBox, json
from Tkinter import *
import ttk
#My packages
from database.queries import getChampionStats
from database.updates import loadNewMatches
from database.models import *
from utilities.constants import constants, champions
from utilities.inout import printHtmlTable
from view.view import MainWindow

js={}
try:
	config = open('config.json')
	js = json.load(config) 
	config.close()
except IOError:
	js['lolkingUrl'] = constants['lolkingUrl']
	


setup_all()
create_all()
window=MainWindow(js)
window.mainloop()

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

js['lolkingUrl']=window.getUpdatedLolkingUrl()
config = open('config.json','w')
json.dump(js, config, sort_keys=True, indent=4)
config.close()
print "#Lata!"