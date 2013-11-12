#Libs
import tkMessageBox
from Tkinter import *
import ttk

def callback():
	try:
		js['lolkingUrl']=e.get()
		tkMessageBox.showinfo(
			"Ok Url",
			"Url loaded successfully"
		)
	except requests.exceptions.MissingSchema:
		tkMessageBox.showerror(
			"Wrong Url",
			"Cannot open provided url"
		)

def getData():
	try:
		loadNewMatches(js)
		tkMessageBox.showinfo(
			"Ok Url",
			"data downloaded successfully"
		)
	except requests.exceptions.MissingSchema:
		tkMessageBox.showerror(
			"Wrong Url",
			"Cannot open provided url"
		)

class MainWindow:
	def __init__(self,js):
		master = Tk('LolNormalStats')
		master.title('LolNormalStats')
		w=master.winfo_screenwidth()
		h=master.winfo_screenheight()
		master.geometry("300x100+%d+%d" % ( (w-300)/2, (h-100)/2 ) )
		w = Label(master, text="Your lolking url:")
		w.grid(columnspan=2)

		e = Entry(master, width=50)
		e.insert(0, js['lolkingUrl'])
		e.grid(columnspan=2)

		e.focus_set()

		b = Button(master, text="Load lolking url", command=callback)
		b.grid(row=2, column=0)


		b2 = Button(master, text="Get data", command=getData)
		b2.grid(row=2, column=1)

	def mainloop(self):
		mainloop()
