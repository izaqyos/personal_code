# This is a much more sophisticated example using more of Tkinter's
# features to show how to create a new custom class of widgets called
# MinMax made of two Entry widgets and a Scale widget.  When more that
# one widget are combined to make a more complex one, it is called a
# "compound widget". The Entry widgets hold the minimum and maximum
# values of the scale. When the user changes these values, the Scale
# is updated.  
# compound widget that allows the user to set the min and max values of a scale

from Tkinter import *

class MinMax(Frame):
    def __init__(self,master,min=1, max=10, command=None):
        Frame.__init__(self,master)
        self.min = StringVar()
        self.min.set(str(min))

        self.minEntry = Entry(self,width=4,textvariable=self.min)
        self.minEntry.bind("<Return>",self.minHandler)
        self.minEntry.bind("<Leave>",self.minHandler)
        self.minEntry.pack(side=LEFT)

        self.heightvalue = DoubleVar()
        self.heightScale = Scale(self, from_=1,  to=10, resolution=.1, orient=HORIZONTAL,
                                 command=command, variable=self.heightvalue)
        self.heightScale.pack(side=LEFT)

        self.max = StringVar()
        self.max.set(str(max))
        self.maxEntry = Entry(self,width=4,textvariable=self.max)
        self.maxEntry.bind("<Return>",self.maxHandler)
        self.maxEntry.bind("<Leave>",self.maxHandler)
        self.maxEntry.pack(side=LEFT)

    def minHandler(self,event):
        newmin = float( self.min.get() )
        oldmin = float(self.heightScale.cget('from'))
        max = float(self.heightScale.cget('to'))
        if newmin < max:
            self.heightScale.config(from_= newmin, resolution=(max-newmin)/100.0)
            if newmin>self.heightvalue.get():
                self.heightScale.set(newmin)
        else:
            self.min.set(str(oldmin))
        
    def maxHandler(self,event):
        newmax = float( self.max.get() )
        oldmax = float(self.heightScale.cget('to'))
        min = float(self.heightScale.cget('from'))
        if newmax > min:
            self.heightScale.config(to = newmax, resolution=(newmax-min)/100.0)
            if newmax<self.heightvalue.get():
                self.heightScale.set(newmax)

class App:

    def __init__(self, root):
        MinMax(root,1,100,command=self.handlewidget).pack(side=TOP)

        #make a label which shows the current value of the MinMax scale widget
        self.label = Label(root,relief=GROOVE)
        self.label.pack(side=BOTTOM)

    def handlewidget(self,value):
        self.label.configure(text=str(value))

toplevel = Tk()

app = App(toplevel)

toplevel.mainloop()

