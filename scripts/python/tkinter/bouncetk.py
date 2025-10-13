from visual import *
from Tkinter import *

scene.range=10
scene.center=(0,5,0)

v  = 0      #initial velocity
dt = 1/30.0 # delta t
y  = 10     # initial position
g  = 0
#setup objects in the scene
ball   = sphere(pos=(0,y,0), color=(1,0,0))
ground = box(pos=(0,0,0), size=(20,.2,20), color=(0,1,0))


print "ball radius=",ball.radius
print "box thickness=",ground.size.y


def step():
    global v
    ball.y = ball.y + v*dt
    v = v - g*dt
    # bounce if one radius from the ground
    if ball.y<(ball.radius+ground.size.y/2):
        ball.y=ball.radius
        v = -v
    scale.after(int(1000*dt),step)

def setg(newg):
    global g
    g = float(newg)

root = Tk()
scale = Scale(root,from_=-10,to=10,command=setg)
scale.set(9.8)
scale.after(int(1000*dt),step)
scale.pack()

root.mainloop()
