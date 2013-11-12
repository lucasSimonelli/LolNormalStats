#Libs
import tkMessageBox
from Tkinter import *
import ttk, requests #Todo: redefine exception in inout and import that

#Packages
from database.updates import loadNewMatches


class MainWindow:
	def __init__(self,js):
		self.js = js
		self.master = Tk('LolNormalStats')
		self.master.title('LolNormalStats')
		w=self.master.winfo_screenwidth()
		h=self.master.winfo_screenheight()
		self.master.geometry("300x100+%d+%d" % ( (w-300)/2, (h-100)/2 ) )
		w = Label(self.master, text="Your lolking url:")
		w.grid(columnspan=2)

		self.e = Entry(self.master, width=50)
		self.e.insert(0, js['lolkingUrl'])
		self.e.grid(columnspan=2)

		self.e.focus_set()

		b = Button(self.master, text="Load lolking url", command=self.callback)
		b.grid(row=2, column=0)


		b2 = Button(self.master, text="Get data", command=self.getData)
		b2.grid(row=2, column=1)

	def mainloop(self):
		mainloop()

	def getData(self):
		try:
			loadNewMatches(self.js)
			tkMessageBox.showinfo(
				"Ok Url",
				"data downloaded successfully"
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
		except requests.exceptions.MissingSchema:
			tkMessageBox.showerror(
				"Wrong Url",
				"Cannot open provided url"
			)

	def getUpdatedLolkingUrl(self):
		return self.js['lolkingUrl']