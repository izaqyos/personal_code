#!/usr/bin/python
# File: widgets.py
# Author: Yosi Izaq
# Description: Example of Tkinter widgets.
#
# Thanks to excellent tutorial at: http://www.pythonware.com/library/tkinter/introduction/
# and http://www.python.org/doc/life-preserver/


from Tkinter import *

class App:

	def __init__(self, master):

		frame = Frame(master)
		frame.pack()

		#Two buttons
		self.button = Button(frame, text="QUIT", fg="red", command=frame.quit)
		self.button.pack(side=LEFT)

		self.hi_there = Button(frame, text="Hello", command=self.say_hi)
		self.hi_there.pack(side=LEFT)

		#Canvas
		w = Canvas(master, width=600, height=600)
		w.pack()

		w.create_text(100,15,  text="Canvas")
		w.create_line(0, 20, 200, 100)
		w.create_line(0, 100, 200, 0, fill="red", dash=(4, 4))

		w.create_rectangle(50, 25, 150, 75, fill="blue")

		may_photo = PhotoImage(file="May1.gif")
		#Keep extra reference to avoid garbage collector deleting the pic
		label = Label(image=may_photo)
		label.image = may_photo # keep a reference!
		#label.pack()
		w.create_image(250, 400, image=label.image)


		#Checkbutton
		self.var = IntVar()
	        c = Checkbutton(master, text="Check button", variable=self.var, command=self.cb)
		c.pack(side=RIGHT)

		#Entry (for text)
		content = StringVar()
		entry = Entry(master,  textvariable=content)
		text = content.get()
		content.set("Entry")
		entry.pack(side=RIGHT)

		#Label
		label1 = Label(master, text="Helvetica Label", font=("Helvetica", 16), fg="red").pack(side=RIGHT)
		label1 = Label(master, text="Helvetica Label", font=("Helvetica", 16), fg="green", bitmap="hourglass").pack(side=RIGHT)

		#list box
		listbox = Listbox(master)
	        listbox.insert(END, "a list entry")
	        for item in ["one", "two", "three", "four"]:
		        listbox.insert(END, item)
		listbox.pack()
		b = Button(master, text="Delete", command=lambda listbox=listbox: listbox.delete(ANCHOR)).pack()


		#Top level menu
		# create a toplevel menu
#		menubar = Menu(master)
#		menubar.add_command(label="Hello!", command=self.say_hi)
#		menubar.add_command(label="Quit!", command=root.quit)
		menubar = Menu(master)

		# create a pulldown menu, and add it to the menu bar
		filemenu = Menu(menubar, tearoff=0)
		filemenu.add_command(label="Open", command=self.hello)
		filemenu.add_command(label="Save", command=self.hello)
		filemenu.add_separator()
		filemenu.add_command(label="Exit", command=root.quit)
		menubar.add_cascade(label="File", menu=filemenu)

		# create more pulldown menus
		editmenu = Menu(menubar, tearoff=0)
		editmenu.add_command(label="Cut", command=self.hello)
		editmenu.add_command(label="Copy", command=self.hello)
		editmenu.add_command(label="Paste", command=self.hello)
		menubar.add_cascade(label="Edit", menu=editmenu)

		helpmenu = Menu(menubar, tearoff=0)
		helpmenu.add_command(label="About", command=self.about)
		menubar.add_cascade(label="Help", menu=helpmenu)

		# display the menu
		root.config(menu=menubar)

#Radio button
		MODES = [
			("Monochrome", "1"),
			("Grayscale", "L"),
			("True color", "RGB"),
			("Color separation", "CMYK"),
		]

		self.var1 = StringVar()
		self.var1.set("L") # initialize

		for text, mode in MODES:
			button2 = Radiobutton(master, text=text,
					variable=self.var1, value=mode, command=self.printChoice())
			button2.pack(side=RIGHT)


	def cb(self):
	        print "variable is", self.var.get()

	def printChoice(self):
	        print "choice is", self.var1.get()

	def say_hi(self):
		print "hi there, everyone!"

	def hello(self):
		print "Hello world."

	def about(self):
		print "Small utility that demonstrates TKinter widgets by Yosi Izaq"

root = Tk()

app = App(root)

root.mainloop()

