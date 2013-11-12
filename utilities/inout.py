import HTML

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
