#Libs
import tkMessageBox
from Tkinter import *
import ttk, tkFont, Image, requests, ImageTk,time #Todo: redefine exception in inout and import that

#Packages
from database.updates import loadNewMatches
from utilities.inout import printAllStatsToHtml, updateLolkingUrl, SummonerNotFound

class MainWindow:
	def __init__(self,js):
		self.js = js
		self.url = ""
		self.master = Tk('LolNormalStats')
		self.master.title('LolNormalStats')
		self.master.resizable(0,0)
		self.customFont = tkFont.Font(family="Helvetica", size=20)
		w=self.master.winfo_screenwidth()
		h=self.master.winfo_screenheight()
		wid = 300
		hei = 450
		self.master.geometry(str(wid)+"x"+str(hei)+"+%d+%d" % ( (w-wid)/2, (h-hei)/2 ) )
		self.master.bind('<Escape>', self.end)
		self.master.grid()
		frame = Frame(self.master)
		frame.pack(fill="both", expand=True, padx=20, pady=20)
		#Title
		title = Label(frame, text="Lol Normal Stats", font=self.customFont)
		title.grid(row=0,columnspan=4)

		#Image
		#TODO: error check
		try:
			im = Image.open('img/lol.png')
			self.tkimage = ImageTk.PhotoImage(im)
			Label(frame, image=self.tkimage).grid(row=1, columnspan=4) 
		except IOError:
			pass

		#Label
		w = Label(frame, text="Username:")
		w.grid(row=3, column=0, sticky='e')

		#Text entry
		self.e = Entry(frame)
		self.e.insert(0, js['username'])
		self.e.grid(row=3, column=1,sticky='w')
		self.e.focus_set()

		#Label sv
		w2 = Label(frame, text="Server:")
		w2.grid(row=4, column=0, sticky='e')

		#Selector sv
		self.sv=StringVar()
		self.sv.set(js['server'])
		separator = OptionMenu(frame, self.sv, "las","lan","na","euw","eune","br","tr","ru","oce")
		separator.grid(row=4, column=1, sticky='w')
		
		#Buttons
		b3 = Button(frame, text="Start", command=self.end)
		b3.grid(row=5, columnspan=6, pady=6)

	def end(self):
		self.js['username'] = self.e.get()
		self.js['server'] = self.sv.get()
		try:
			self.url = updateLolkingUrl(self.e.get(), self.sv.get(), self.js)
		except SummonerNotFound:
			tkMessageBox.showerror(
				"Summoner not found",
				"Summoner name "+self.js['username']+ " was not found in "+ self.js['server'].upper()
			)
			return
		tkMessageBox.showinfo(
			"Ok",
			"Summoner found, starting data download"
		)
		self.master.destroy()

	#Hide self.master.withdraw() show: self.master.update()	self.master.deiconify() 
	def mainloop(self):		
		mainloop()

	def getUsername(self):
		return self.js['username']

	def getServer(self):
		return self.js['server']

	def getUrl(self):
		return self.url

	def updateUrl(self):
		if updateLolkingUrl(self.e.get(),self.js):
			tkMessageBox.showinfo(
				"Ok Url",
				"Summoner found, starting data download"
			)
		else:
			tkMessageBox.showerror(
				"Wrong Url",
				"The provided summoner name was not found in the given region"
			)
