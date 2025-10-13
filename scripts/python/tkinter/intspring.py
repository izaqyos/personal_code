from time import sleep
from threading import Thread
from Tkinter import *
from springkutta import SpringPendulum

class App:

    def __init__(self, master):

      
        frame = Frame(master)
        frame.pack()

        self.goButton = Button(frame, text="Go!", command=self.goHandler)
        self.goButton.pack(side=LEFT)

        self.posScale = Scale(frame, from_=0, to=3.141, resolution=.1,
                              command=self.scaleHandler, orient=HORIZONTAL)
        self.posScale.pack(side=BOTTOM)

        self.pendulum  = SpringPendulum(1/30.0)
        self.pendulum.spring.damping=0
        self.pendulum.display.autoscale = 0
        self.pendulum.display.center    = (0,-2,0)
        self.pendulum.display.range     = 3

        self.updating=False
        self.posScale.after(33,self.idlecallback)                                                 
        
    def idlecallback(self):
        if not self.updating:
            self.pendulum.simulate()
            self.posScale.after(33,self.idlecallback)                                                 

    def scaleHandler(self,newvalue):
        self.updating=True
        self.pendulum.theta=float(newvalue)

    def goHandler(self):
        self.updating=False
        self.posScale.after(33,self.idlecallback)                                                 



root = Tk()

app = App(root)

root.mainloop()

