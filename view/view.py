#Libs
import tkMessageBox
from Tkinter import *
import ttk, tkFont, Image, requests, ImageTk,time #Todo: redefine exception in inout and import that

#Packages
from database.updates import loadNewMatches
from utilities.inout import printAllStatsToHtml, updateLolkingUrl

class MainWindow:
	def __init__(self,js):
		self.js = js
		self.master = Tk('LolNormalStats')
		self.master.title('LolNormalStats')
		self.master.resizable(0,0)
		self.customFont = tkFont.Font(family="Helvetica", size=20)
		w=self.master.winfo_screenwidth()
		h=self.master.winfo_screenheight()
		wid = 340
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
		w = Label(frame, text="Your lolking url:")
		w.grid(columnspan=2, sticky='w')

		#Text entry
		self.e = Entry(frame, width = 50)
		self.e.insert(0, js['lolkingUrl'])
		self.e.grid(row=3,column=0,columnspan=3,sticky='w')
		self.e.focus_set()

		#Separator
		separator = Frame(frame)
		separator.grid(row=4, padx=5, pady=5)
		
		#Buttons
		#b2 = Button(frame, text="Update lolking url", command=self.updateUrl)
		#b2.grid(row=5, column=0)
		b3 = Button(frame, text="Start", command=self.end)
		b3.grid(row=5, column=2)

	def end(self):
		if not updateLolkingUrl(self.e.get(),self.js):
			tkMessageBox.showerror("Wrong Url","Cannot open provided url")
			return
		tkMessageBox.showinfo("Ok Url","Url set, starting program")
		self.master.destroy()

	#Hide self.master.withdraw() show: self.master.update()	self.master.deiconify() 
	def mainloop(self):		
		mainloop()


	def updateUrl(self):
		if updateLolkingUrl(self.e.get(),self.js):
			tkMessageBox.showinfo(
				"Ok Url",
				"Url set"
			)
		else:
			tkMessageBox.showerror(
				"Wrong Url",
				"You didn't provide a valid lolking url"
			)

	def getUpdatedLolkingUrl(self):
		return self.js['lolkingUrl']