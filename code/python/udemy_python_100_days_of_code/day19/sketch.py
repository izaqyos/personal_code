#!/opt/homebrew/bin/python3
from turtle import Turtle, Screen
from functools import partial

def go_fwd(a_turtle, steps=10):
    a_turtle.fd(steps)

def go_back(a_turtle, steps=10):
    a_turtle.bk(steps)

def set_tilt(a_turtle, angel):
    a_turtle.tilt(angel)
    a_turtle.seth(a_turtle.heading()+angel)

def clear_screen(a_turtle):
    a_turtle.clear()
    a_turtle.penup()
    a_turtle.home()
    a_turtle.pendown()

def help_message():
    print("This is a simple sketching program")
    print("h- tilt counterclockwise")
    print("j- go forward")
    print("k- go backward")
    print("l- tilt clockwise")
    print("c- clear screen")

def main():
    help_message()
    t = Turtle()
    scr = Screen()

    scr.listen()
    scr.onkey(fun=partial(go_fwd, t, 10), key="j" )
    scr.onkey(fun=partial(go_back, t, 10), key="k" )
    scr.onkey(fun=partial(set_tilt, t, 10), key="h" )
    scr.onkey(fun=partial(set_tilt, t, -10), key="l" )
    scr.onkey(fun=partial(clear_screen, t), key="c" )

    scr.exitonclick()

if __name__ == "__main__":
    main()


