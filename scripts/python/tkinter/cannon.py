from visual import *
from Tkinter import *
from cannonworld import *
import sys

scene.forward=(-.4,-.4,-1)
scene.autoscale=0
scene.range=50

class Application:
    def __init__(self,root,framerate=100):
        self.world=World()
        self.cannon=Cannon(self.world)
        ground = box(pos=(50,0,50),size=(100,.1,100), color=color.green)

        self.frame = Frame(root)
        self.frame.pack()

        self.button = Button(self.frame, text="FIRE!", fg="red", command=self.cannon.fire)
        self.button.pack(side=BOTTOM)
        
        self.anglescale = Scale(self.frame, from_=0, to=pi/2, resolution=.1, label="direction", command=self.changeangle, orient=HORIZONTAL)
        self.anglescale.set(pi/4)
        self.anglescale.pack(side=BOTTOM)

        self.pitchscale = Scale(self.frame, from_=0, to=pi/2, resolution=.1, label="pitch", command=self.changepitch, orient=VERTICAL)
        self.pitchscale.set(pi/4)
        self.pitchscale.pack(side=RIGHT)        

        self.vscale = Scale(self.frame, from_=1, to=40, resolution=1, label="velocity", command=self.changevelocity, orient=VERTICAL)
        self.vscale.set(20)
        self.vscale.pack(side=RIGHT)        

        # setup continuous update of cannon world
        self.dt=1.0/framerate
        self.timeout=int(self.dt*1000)
        self.button.after(self.timeout,self.idlecallback)

    def changeangle(self,event):
        print "changeangle()"
        self.cannon.angle = self.anglescale.get()
        self.cannon.aim()

    def changepitch(self,event):
        print "changepitch()"
        self.cannon.pitch = self.pitchscale.get()
        self.cannon.aim()

    def changevelocity(self,event):
        self.cannon.vinitial = self.vscale.get()

    def idlecallback(self):
        self.world.step(self.dt)
        self.button.after(self.timeout,self.idlecallback)                                                   

    def exit(self):
        scene.visible=0
        self.frame.quit()



root = Tk()

app = Application(root)

root.mainloop()


