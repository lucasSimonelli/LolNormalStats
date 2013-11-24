import HTML, requests, os, re
from lxml import html

from utilities.constants import constants, champions
from database.queries import getChampionStats
from utilities.misc import findBetween


#Returns a list of lists, the first one containing the keys and the second one the values
def dictToListOfLists(dict):
	output = []
	l=[]
	for key in dict.keys():
		l.append(key)
	output.append(l)
	auxList=[]
	for key in dict.keys():
		auxList.append(dict[key])
	output.append(auxList)
	return output


#Given a list of lists outputs an html table to the current dir
def printHtmlTable(list):
	if len(list)>0:
		htmlcode = HTML.table(list[1:],header_row=list[0])
		f = open("out.html","a")
		f.write(htmlcode)
		f.close()


def loadLolkingHTML(json):
	r = requests.get(json['lolkingUrl'])

	historyHTML = findBetween(r.text,constants['startTrim'],constants['endTrim'])
	historyHTML = historyHTML.rstrip('\n')[3:-2] #Removing \n hardcodily.
	parsed = html.fromstring(historyHTML)
	return parsed


def printStatsToHtml(gamemode):
	directory = 'stats'
	if not os.path.exists(directory):
   		os.makedirs(directory)
	
	try:
		head = open('templates/header.html')
		htmlHead = head.read()
		head.close()
	except IOError:
		#TODO: Log error
		return

	try:
		foot = open('templates/footer.html')
		htmlFooter = foot.read()
		foot.close()
	except IOError:
		#TODO: Log error
		return

	f = open(directory+'/'+gamemode+'-stats.html','w')
	f.write(htmlHead % (gamemode,gamemode))
	for champion in champions:
		dict=getChampionStats(champion.lower(), gamemode)
		if dict==None:
			continue	
		f.write("<tr>")
		f.write("<td style=\"white-space: nowrap;\"><img src=\"../img/icons/"+dict['champion'].title()+".png\" />  "+dict['champion'].title()+"</td>")
		f.write("<td>"+str(float(dict['kills']/(dict['wins']+dict['losses'])))+"</td>")
		f.write("<td>"+str(float(dict['deaths']/(dict['wins']+dict['losses'])))+"</td>")
		f.write("<td>"+str(float(dict['assists']/(dict['wins']+dict['losses'])))+"</td>")
		f.write("<td>"+str(float(dict['minions']/(dict['wins']+dict['losses'])))+"</td>")
		f.write("<td>"+str(float(dict['gold']/(dict['wins']+dict['losses'])))+"</td>")
		f.write("<td>"+str(dict['wins'])+"</td>")
		f.write("<td>"+str(dict['losses'])+"</td>")
		f.write("</tr>")

	f.write(htmlFooter)
	f.close()


def printAllStatsToHtml():
	printStatsToHtml(constants['normal'])
	printStatsToHtml(constants['aram'])
	printStatsToHtml(constants['rankedTeam'])
	printStatsToHtml(constants['soloQ'])
	printStatsToHtml(constants['custom'])

expr = r'http://www.lolking.net/summoner/[a-z][a-z]{1,3}/[0-9]+'

def validateLolkingUrl(string):
	m = re.match(expr,string)
	if m:
		return True
	return False

def updateLolkingUrl(newUrl,dict):
	if not validateLolkingUrl(newUrl):
		return False
	dict['lolkingUrl']=newUrl
	return True
