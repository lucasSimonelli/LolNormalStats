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

a={ 'a':1, 'b':2}

print dictToListOfLists(a)
