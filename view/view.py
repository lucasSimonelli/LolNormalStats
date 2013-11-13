#Libs
import tkMessageBox
from Tkinter import *
import ttk, requests #Todo: redefine exception in inout and import that

#Packages
from database.updates import loadNewMatches
from utilities.inout import printAllStatsToHtml

class MainWindow:
	def __init__(self,js):
		self.js = js
		self.master = Tk('LolNormalStats')
		self.master.title('LolNormalStats')
		w=self.master.winfo_screenwidth()
		h=self.master.winfo_screenheight()
		wid = 310
		hei = 80
		self.master.geometry(str(wid)+"x"+str(hei)+"+%d+%d" % ( (w-wid)/2, (h-hei)/2 ) )
		self.master.bind('<Escape>', self.end)
		w = Label(self.master, text="Your lolking url:")
		w.grid(columnspan=2, sticky='w')

		self.e = Entry(self.master, width = 50)
		self.e.insert(0, js['lolkingUrl'])
		self.e.grid(row=1,column=0,columnspan=3,sticky='w')

		self.e.focus_set()

		b = Button(self.master, text="Load lolking url", command=self.callback)
		b.grid(row=2, column=0)


		b2 = Button(self.master, text="Get data", command=self.getData)
		b2.grid(row=2, column=1)

		b3 = Button(self.master, text="Crunch them stats", command=self.crunchStats)
		b3.grid(row=2, column=2)


	def end(self,master):
		self.master.destroy()

	def mainloop(self):
		mainloop()

	def getData(self):
		try:
			loadNewMatches(self.js)
			tkMessageBox.showinfo(
				"Ok Url",
				"Data downloaded successfully"
			)
		except requests.exceptions.MissingSchema:
			tkMessageBox.showerror(
				"Wrong Url",
				"Cannot open provided url"
			)

	def callback(self):
		try:
			self.js['lolkingUrl']=self.e.get()
			tkMessageBox.showinfo(
				"Ok Url",
				"Url loaded successfully"
			)
		except requests.exceptions.MissingSchema:#TODO: regexp check the url
			tkMessageBox.showerror(
				"Wrong Url",
				"Cannot open provided url"
			)


	def crunchStats(self):
		printAllStatsToHtml()
		tkMessageBox.showinfo(
			"Stats crunched",
			"Stats crunched! Check the stats/ folder"
		)

	def getUpdatedLolkingUrl(self):
		return self.js['lolkingUrl']