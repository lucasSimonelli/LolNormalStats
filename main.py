#Libs
import json

#My packages
from database.queries import getChampionStats
from database.updates import loadNewMatches
from database.models import *
from utilities.constants import constants
from utilities.inout import printHtmlTable, printStatsToHtml
from view.view import MainWindow

js={}
try:
	config = open('config.json','r')
	js = json.load(config) 
	config.close()
except IOError:
	js['lolkingUrl'] = constants['lolkingUrl']
	


setup_all()
create_all()
window=MainWindow(js)
window.mainloop()


printStatsToHtml(constants['normal'])
printStatsToHtml(constants['aram'])
printStatsToHtml(constants['rankedTeam'])
printStatsToHtml(constants['soloQ'])
printStatsToHtml(constants['custom'])


js['lolkingUrl']=window.getUpdatedLolkingUrl()
config = open('config.json','w')
json.dump(js, config, sort_keys=True, indent=4)
config.close()
print "#Lata!"