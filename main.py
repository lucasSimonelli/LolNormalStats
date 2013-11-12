#Libs
import json

#My packages
from database.queries import getChampionStats
from database.updates import loadNewMatches
from database.models import *
from utilities.constants import constants, champions
from utilities.inout import printHtmlTable, htmlHead, htmlFooter
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

f = open('stats.html','w')
f.write(htmlHead)
for champion in champions:
	dict=getChampionStats(champion.lower(), constants['normal'])
	if dict==None:
		continue	
	f.write("<tr>")
	for key in dict.keys():
		if key != 'id':
			if key.lower() == 'champion':
				f.write("<td><img src=\"img/icons/"+dict[key].title()+".png\" />  "+dict[key].title()+"</td>")
			else:
				f.write("<td>"+str(dict[key])+"</td>")
	f.write("</tr>")

f.write(htmlFooter)
f.close()
js['lolkingUrl']=window.getUpdatedLolkingUrl()
config = open('config.json','w')
json.dump(js, config, sort_keys=True, indent=4)
config.close()
print "#Lata!"