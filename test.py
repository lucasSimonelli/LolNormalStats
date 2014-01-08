import HTML, requests, os, re
from lxml import html


def getLolkingPermalink(username, userServer):
	exprLink = r'.*(summoner/.*/[0-9]+).*'
	exprSv = r'.*summoner/(.*)/.*'
	r = requests.get("http://www.lolking.net/search?name="+username)
	htmlResponse = html.fromstring(r.text)
	items = htmlResponse.xpath("//div[@class='search_result_item']")
	link = "a/"
	for element in items:
		text = element.get('onclick')
		server = re.search(exprSv, text).group(1)
		if server == userServer:
			link += re.search(exprLink, text).group(1)
			break

	return link
	
getLolkingPermalink("DreamMirrors","las")