import HTML, requests
from lxml import html

from utilities.constants import constants
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


htmlHead = """
<html lang="en">
<head>
<title>Normal game performance</title>

<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.4/jquery.min.js"></script>
<script type="text/javascript">
 $(function() {
		/* For zebra striping */
        $("table tr:nth-child(odd)").addClass("odd-row");
		/* For cell text alignment */
		$("table td:first-child, table th:first-child").addClass("first");
		/* For removing the last border */
		$("table td:last-child, table th:last-child").addClass("last");
});
</script>

<link rel="stylesheet" type="text/css" href="templates/style.css"/>


</head>
<body>
<div style="text-align:center;font-size:30;">
<br>
<h1>Normal game performance</h1>
</div>
<div id="content">

    <table cellspacing="0">
    <tr><th>Champion</th><th>Kills</th><th>Deaths</th><th>Wins</th><th>Losses</th><th>Assists</th><th>Gold</th><th>Minions</th></tr>

"""

htmlFooter = """    </table>

</div>

</body>
</html>
"""