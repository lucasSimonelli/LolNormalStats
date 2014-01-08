#Libs
import json, time, shutil, os

#My packages
from database.queries import getChampionStats
from database.updates import loadNewMatches
from database.models import *
from utilities.constants import constants
from utilities.inout import printAllStatsToHtml
from view.view import MainWindow

DELAY = 5*3600 #Every 5 hours

#Copy file to auto startup this shit
direct = os.getcwd()
#shutil.copy2('/dir/file.ext', '/new/dir/newname.ext')
config={}
try:
	configFile = open('config.json','r')
	config = json.load(configFile) 
	configFile.close()
except (IOError, ValueError):
	config['username'] = constants['defaultUser']
	config['server'] = constants['defaultServer']


setup_all()
create_all()
window=MainWindow(config)
window.mainloop()
config['username'] = window.getUsername()
config['server'] = window.getServer()
lolkingUrl = window.getUrl()
configFile = open('config.json','w')
json.dump(config, configFile, sort_keys=True, indent=4)
configFile.close()

while True:
	loadNewMatches(lolkingUrl)
	printAllStatsToHtml()
	print "Download successful"
	print "Waiting for "+ str(DELAY/3600)+" hours to perform new query"
	time.sleep(DELAY)
	


print "#Lata"