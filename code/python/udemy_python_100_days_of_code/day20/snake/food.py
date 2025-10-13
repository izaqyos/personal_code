from turtle import Turtle
import random

class Food(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.penup()
        self.shapesize(stretch_len=0.5, stretch_wid=0.5) #10X10 size instead of default 20X20
        self.color("purple")
        self.speed("fastest") #so we don't see food slowly animated on screen
        self.refresh()

    def refresh(self):
        self.goto(random.randint(-270,270) , random.randint(-270,270))
