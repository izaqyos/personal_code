from turtle import Turtle
import time


class Snake:

    def __init__(self, move_length=20):
        print(f"Snake CTOR called")
        self.move_length = move_length
        self.initial_length = 3  # number of turtles, assume each turtle is 20X20 in size
        self.create_snake()
    
    def create_snake(self):
        self.turtles = []
        self.direction = "forward"
        for i in range(self.initial_length):
            self.extend()

    def reset(self):
        for turtle in self.turtles:
            turtle.goto(1000,1000)
            #turtle.clear()
            #del turtle
        self.turtles.clear()
        self.create_snake()

    def _add_segment(self):
        length = len(self.turtles)
        t = Turtle(shape="square")
        self.turtles.append(t)
        x, y = t.pos()
        t.color("white")
        t.penup()
        #print(f"_add_segment(), adding segment {length+1}, at coordinates {(x+(-self.move_length * (length)), y)} ")
        t.goto(x+(-self.move_length * (length)), y)

    def extend(self):
        self._add_segment()

    def get_segments(self):
        return self.turtles

    def get_head(self):
        return self.turtles[0]

    def move(self, direction="fwd"):
        #print(f"snake::move() moving length {self.move_length}")
        #self.printme()
        for i in range(len(self.turtles)-1, 0, -1):
            self.turtles[i].penup()
            self.turtles[i].goto(self.turtles[i-1].pos())
        self.turtles[0].fd(self.move_length)

    def move_naive(self, direction="fwd", length=20):
        #for now ignore direction, assume fwd
        for t in self.turtles:
            t.penup()
            t.fd(len(self.turtles))

    def up(self):
        #print("Snake::up() called")
        if self.direction != "down":
            self.turtles[0].seth(90) #change to heading
            self.direction = "up"

    def down(self):
        #print("Snake::down() called")
        if self.direction != "up":
            self.turtles[0].seth(270) #change to heading
            self.direction = "down"

    def left(self):
        #print("Snake::left() called")
        if self.direction != "right":
            self.turtles[0].seth(180) #change to heading
            self.direction = "left"

    def right(self):
        #print("Snake::right() called")
        if self.direction != "left":
            self.turtles[0].seth(0) #change to heading
            self.direction = "right"
        pass

    def printme(self):
        print(f"snake length is {len(self.turtles)}. Segments locations:")
        for i,t in enumerate(self.turtles):
            print(f"segment[{i}] location {t.pos()}")

