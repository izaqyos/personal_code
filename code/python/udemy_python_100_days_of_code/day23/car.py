from turtle import Turtle
from random import randint

class Car(Turtle):
    def __init__(self, logger, screen, color, starting_move_distance, move_increment):
        super().__init__()
        self.logger = logger
        self.starting_move_distance = starting_move_distance
        self.set_speed(starting_move_distance)
        self.move_increment = move_increment
        self.logger.info(f"Initializing car")
        self.screen = screen
        self.ht() 
        self.shape("square")
        self.color(color)
        self.shapesize(stretch_wid=1, stretch_len=2)
        self.penup()
        self.set_init_pos()
        self.st() 

    def set_init_pos(self): 
        xcor, ycor = 300, randint(-260, 260)
        starting_position = (xcor, ycor)
        self.goto(starting_position)

    def move(self):
        x,y = self.pos()
        #self.logger.info(f"Car::move() called. move_distance={self.move_distance}")
        #self.goto(x-self.move_distance, y)
        self.backward(self.move_distance)

    def get_speed(self):
        return self.move_distance

    def set_speed(self, distance):
        self.logger.debug(f"Setting new move distance to {distance}")
        self.move_distance = distance


