#Libs
import json, time

#My packages
from database.queries import getChampionStats
from database.updates import loadNewMatches
from database.models import *
from utilities.constants import constants
from utilities.inout import printHtmlTable, printStatsToHtml
from view.view import MainWindow

DELAY = 5*3600 #Every 5 hours


config={}
try:
	configFile = open('config.json','r')
	config = json.load(configFile) 
	configFile.close()
except IOError:
	config['lolkingUrl'] = constants['lolkingUrl']
	


setup_all()
create_all()
window=MainWindow(config)
window.mainloop()
while True:
	time.sleep(DELAY)
	loadNewMatches(config)

config['lolkingUrl']=window.getUpdatedLolkingUrl()
configFile = open('config.json','w')
json.dump(configFile, config, sort_keys=True, indent=4)
configFile.close()
print "#Lata"