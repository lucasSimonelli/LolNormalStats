import HTML, requests, os, re
from lxml import html

from utilities.constants import constants, champions
from database.queries import getChampionStats
from utilities.misc import findBetween

class SummonerNotFound(Exception):
    pass

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


def loadLolkingHTML(url):
	r = requests.get(url) 
	htmlResponse = html.fromstring(r.text)
	won = htmlResponse.xpath("//div[@class='match_win']")
	lost = htmlResponse.xpath("//div[@class='match_loss']")
	return won+lost


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
		query=getChampionStats(champion.lower(), gamemode)
		if query==None:
			continue	
		
		dict = computeAverageStats(query, champion.lower(), gamemode)
		format = "%0.1f"
		f.write("<tr>")
		f.write("<td style=\"white-space: nowrap;\"><img src=\"../img/icons/"+dict['champion'].title()+".png\" />  "+dict['champion'].title()+"</td>")
		f.write("<td>"+format%float(dict['kills']/float(dict['wins']+dict['losses']))+"</td>")
		f.write("<td>"+format%float(dict['deaths']/float(dict['wins']+dict['losses']))+"</td>")
		f.write("<td>"+format%float(dict['assists']/float(dict['wins']+dict['losses']))+"</td>")
		f.write("<td>"+format%float(dict['minions']/float(dict['wins']+dict['losses']))+"</td>")
		f.write("<td>"+format%float(dict['gold']/float(dict['wins']+dict['losses'])/1000)+"k</td>")
		f.write("<td>"+str(dict['wins'])+"</td>")
		f.write("<td>"+str(dict['losses'])+"</td>")
		f.write("<td>"+format%(dict['wins']*100/float(dict['wins']+dict['losses']))+"%"+"</td>")
		f.write("</tr>")

	f.write(htmlFooter)
	f.close()


def printAllStatsToHtml():
	printStatsToHtml(constants['normal'])
	printStatsToHtml(constants['aram'])
	printStatsToHtml(constants['rankedTeam'])
	printStatsToHtml(constants['soloQ'])
	printStatsToHtml(constants['custom'])
	#printStatsToHtml(constants['oneForAll'])

def validateLolkingUrl(string):
	expr = r'http://www.lolking.net/summoner/[a-z][a-z]{1,3}/[0-9]+'
	m = re.match(expr,string)
	if m:
		return True
	return False

def updateLolkingUrl(username,server,dict):
	newUrl = getLolkingPermalink(username, server)
	return newUrl

def computeAverageStats(query, champion, gameType):
	dict={'champion':champion, 'gameType': gameType, 'wins':0, 'losses':0, 'kills':0, 
		'deaths':0, 'assists':0, 'minions':0, 'gold':0}
	dict['wins'] = 0
	dict['losses'] = 0
	for match in query:
		match = match.to_dict()
		if match['won']:
			dict['wins']+=1
		else:
			dict['losses']+=1
		dict['kills']+=match['kills']
		dict['deaths']+=match['deaths']
		dict['assists']+=match['assists']
		dict['minions']+=match['minions']
		dict['gold']+=match['gold']

	return dict


def getLolkingPermalink(username, userServer):
	exprLink = r'.*(summoner/.*/[0-9]+).*'
	exprSv = r'.*summoner/(.*)/.*'
	r = requests.get("http://www.lolking.net/search?name="+username)
	htmlResponse = html.fromstring(r.text)
	items = htmlResponse.xpath("//div[@class='search_result_item']")
	if len(items)==0:
		raise SummonerNotFound()
	link = constants['lolking']
	for element in items:
		text = element.get('onclick')
		server = re.search(exprSv, text).group(1)
		if server == userServer:
			link += re.search(exprLink, text).group(1)
			break

	return link