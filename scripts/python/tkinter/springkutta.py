from visual import *

class RKSolver:
    def __init__(self,f,g,x,y,dt):
        self.f = f
        self.x = x
        self.y = y
        self.g = g
        self.dt = dt

    def step(self):
        x=self.x; y=self.y
        f=self.f; g=self.g
        dt = self.dt

        k1 = f(x,y)                    ;   j1 = g(x,y)
        k2 = f(x+(dt/2)*k1,y+(dt/2)*j1);   j2 = g(x+(dt/2)*k1,y+(dt/2)*j1)
        k3 = f(x+(dt/2)*k2,y+(dt/2)*j2);   j3 = g(x+(dt/2)*k2,y+(dt/2)*j2)
        k4 = f(x+dt*k3, y+dt*j3)       ;   j4 = g(x+dt*k3, y+dt*j3)
        
        self.x += (dt/6)*(k1+2*k2+2*k3+k4)
        self.y += (dt/6)*(j1+2*j2+2*j3+j4)

        return (x,y)


#This class puts VPython objects added to it with its add() method into a VPython
#   frame object which when positioned or oriented will treat all the objects it
#   contains as a group
class CompositeObject:
    frame=frame(axis=(0,-1,0))

    def add(self,thing):
        'add a new object'
        thing.frame = self.frame


    def setAngle(self,theta):
        'set the angle of the frame with respect to vertical'
        self.frame.axis = (sin(theta), -cos(theta), 0)

    #This special function is called automatically whenever an attribute is referenced
    def __setattr__(self,name,value):
        if name=='axis':
            self.frame.axis=value

        if name=='angle':
            self.setAngle(value)
        else:
            self.__dict__[name]=value # this actually assigns the attribute the new value


            
class Spring:
    curve = curve(radius=0.01) # the visual representation of the spring

    def __init__(self,length=1, rest_length=1, k=10, damping=.8, turns=10):
        self.length      = length
        self.rest_length = rest_length
        self.k           = k       # spring constant (stiffness)
        self.damping     = damping # damping factor (damping due to friction)
        self._helix(length,turns)  # draw the spring

    def _helix(self,length=1, turns=10):
        '''This method draws the visual representation of the spring
           which is a helix from x=0 to x=length centered around x axis'''

        radius=.1 #how big around the turns of the helix are
        x=0
        dx = float(length)/turns/12 # how far forward each point is in X direction
        dtheta=pi/6 # angle between successive points
        points=[]
        for theta in arange(0,2*pi*turns,dtheta):
            z=radius*cos(theta)
            y=radius*sin(theta)
            points.append((x,y,z))
            x += dx
        self.curve.pos = points

    def __setattr__(self,name,value):
        if name=='frame':
            self.curve.frame=value
        elif name=='length':
            self._helix(value)
        self.__dict__[name]=value




class SpringPendulum(CompositeObject):
    'A class of objects representing a spring fixed at one end with a mass attached to the other'

    def __init__(self,time_interval):

        self.time_interval = time_interval
        self.solver = RKSolver( self.veloEQ,self.accelEQ ,0,0,1) # compute net acceleration
        self.steps=10
        self.spring=Spring()
        self.add( self.spring )
        self.bob = sphere(radius=.2,color=color.red, pos=(self.spring.length,0,0))
        self.pos = vector(0,-self.spring.length,0)
        self.add(self.bob)
        self.display=self.bob.display
        self.velocity = vector(0,0,0) #velocity vector
        self.solver.x = self.pos
        self.solver.y = self.velocity

    def accelEQ(self,p,v):
        g=vector(0,-9.8,0) # acceleration due to gravity
        S = mag(p)-self.spring.rest_length
        return g - self.spring.k*S*norm(p) - self.spring.damping*v

    def veloEQ(self,x,v): return v

    def simulate(self):
        '''simulate forward in time using "steps" subintervals using Euler's method'''
        p=self.pos
        v=self.velocity
        
        step=0
        while step<self.steps:
            p,v = self.solver.step()
            step += 1

        #copy final values back into this objects attributes
        self.pos = p
        self.velocity = v
                                         
    def _setPosition(self,position):
        '''change position of the pendulum bob'''
        self.frame.axis=position
        self._setLength(mag(position))
        
    def _setLength(self,l):
        '''change the pendulum's length'''
        self.spring.length=l  # set springs length
        self.bob.pos=(l,0,0)  # update the bob's position
        self.__dict__['pos']=l*norm(self.pos)
        self.solver.x = self.pos

    def __setattr__(self,name,value):
        self.__dict__[name]=value
        if name=='pos':
            self._setPosition(value)
        elif name=='length':
            self._setLength(value)
        elif name=='steps':
            dt = float(self.time_interval)/value
            self.solver.dt = dt
        elif name=='theta':
            CompositeObject.setAngle(self,value)
            self.pos = vector(self.spring.length*sin(value),-self.spring.length*cos(value),0)
