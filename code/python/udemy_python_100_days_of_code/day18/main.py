from random import choice, randrange, randint
from turtle import Turtle, Screen
import turtle as t
t.colormode(255) #allow pencolor r,g,b values from 0-255


class TurtleBasics:
    def __init__(self, turtle_obj):
        self.write_callcount = 0
        self.write_startx, self.write_starty = -500 , +500
        self.t = turtle_obj
        self.colors = ["magenta3", "dark sea green", "violet red", "dark violet", "royal blue", "cyan2", "gold2"]

    def _set_rand_color_from_premade_list(self):
        self.t.color(choice(self.colors))

    def set_rand_color(self):
        #self._set_rand_color_from_premade_list()
        self._set_rand_color()

    def _set_rand_color(self):
        color_tuple = self._get_rand_rgb_tuple()
        print(f"setting pencolor to {color_tuple}")
        #self.t.pencolor(color_tuple)
        self.t.color(color_tuple)

    def _get_rand_rgb_tuple(self):
        return  ( randint(0,255) , randint(0,255) , randint(0,255) )  # r,g,b random values tuple


    def write_text(self, text):
        self.set_rand_color()
        self.write_startx = self.write_startx 
        self.write_starty = self.write_starty - (self.write_callcount*30)
    
        self.t.penup()
        self.t.goto(self.write_startx, self.write_starty )
        self.t.pendown()
    
        #print(f"turtl position is {self.write_startx},{self.write_starty}")
        self.t.write(text, False, align="left", font=('Arial', 16, 'bold'))
        self.write_callcount +=1
    
    def draw_spirograph(self, circles = 30):
        self._set_pos_middle()
        #self.t.pd()
        radius = 100
        self.t.speed("fastest")
        print("set speed to fastest")
        for i in range(circles):
            print(f"draw_spirograph, setheading to {i*12}")
            self.set_rand_color()
            self.t.circle(100)
            self.t.setheading(self.t.heading()+360/12) #12 = 360/30
        self.t.speed("normal")
            
    def draw_xtagone(self, sides, side_length):
        self.set_rand_color()
        self.t.pd()
        for j in range(sides):
            self.t.fd(side_length)
            self.t.right(360/sides)

    def draw_xtagones(self, sides=3, max_sides=10, side_length=100):
        for i in range(max_sides+1):
            self.draw_xtagone(i, side_length) 

    def draw_dashed_line(self, repeats, draw_len, no_draw_len):
        self.set_rand_color()
        for i in range(repeats):
            self.t.pendown()
            self.t.fd(draw_len)
            self.t.penup()
            self.t.fd(no_draw_len)
        self.t.pendown()

    def draw_random_walk(self, total_steps=150):
        self._set_pos_middle()
        self.t.pendown()
        self.t.pensize(10)
        self.t.speed("fastest")
        step_length = 20
        def handle_0():
            self.set_rand_color()
            self.t.seth(0)
            self.t.fd(step_length)

        def handle_1():
            self.set_rand_color()
            self.t.seth(90)
            self.t.fd(step_length)

        def handle_2():
            self.set_rand_color()
            self.t.seth(180)
            self.t.fd(step_length)

        def handle_3():
            self.set_rand_color()
            self.t.seth(270)
            self.t.fd(step_length)

        switch_dict = {
                0: handle_0,
                1: handle_1,
                2: handle_2,
                3: handle_3,
        }


        for i in range(total_steps):
            direction = randrange(4) #0, right; 1, down; 2, left; 3- up
            switch_dict[direction]()
        self.t.seth(0)
        self.t.pensize(1)
        self.t.speed("normal")

    def _set_pos_middle(self):
        self.t.home()

    def draw_square(self, length):
        self.set_rand_color()
        if not length:
            length = 100
        for i in range(4):
            self.t.fd(length)
            self.t.rt(90)
    
def main():
    turt = Turtle()
    tb = TurtleBasics(turt)
    screen = Screen()
    turt.shape("turtle")
    #use https://www.tcl.tk/man/tcl8.4/TkCmd/colors.html
    #turt.color("magenta3")
    tb.write_text("Hello Turtle. A few basic examples of using turtle")
    tb.write_text("Draw a spirograph")
    tb.draw_spirograph()
    tb.write_text("Draw a square...")
    #turt.color("dark sea green")
    tb.draw_square(60)
    #turt.color("red")
    tb.write_text("Draw a dashed line...")
    tb.draw_dashed_line(15, 20, 20)
    #turt.color("violet red")
    tb.write_text("Draw xxxtagones...")
    tb.draw_xtagones(3, 10, 100)
    tb.draw_random_walk(300)
    screen.exitonclick()
   

if __name__ == '__main__':
    main()
