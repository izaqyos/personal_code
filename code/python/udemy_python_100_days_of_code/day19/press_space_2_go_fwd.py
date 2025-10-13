#!/opt/homebrew/bin/python3
from turtle import Turtle, Screen
from functools import partial

def go_fwd(a_turtle, steps=10):
    a_turtle.fd(steps)

def main():
    t = Turtle()
    scr = Screen()

    scr.listen()
    scr.onkey(fun=partial(go_fwd, t, 10), key="space" )

    scr.exitonclick()

if __name__ == "__main__":
    main()


