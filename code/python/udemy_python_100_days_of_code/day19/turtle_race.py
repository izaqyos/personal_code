#!/opt/homebrew/bin/python3
from turtle import Turtle, Screen
from functools import partial
import random


def setup(scr, width=500, height=400):
    scr.setup(width, height)

def setup_game(colors):
    turtles = [Turtle(shape="turtle") for _ in colors]
    for i,t in enumerate(turtles):
        t.penup()
        t.color(colors[i])
        t.goto(-240, 190 - (i*70))
    return turtles

def start_race(turtles, user_resp, width, height):
    distance_range = (0,10)
    winner = None
    while user_resp:
        for i,t in enumerate(turtles):
            if t.pos()[0] >= width//2-20: #assume turtle size is 40X40 we declare him winner once he has half crossed the finish line
                return i #we have a winner
            else:
                t.fd(random.randint(*distance_range))

def main():
    #t = Turtle(shape="turtle")
    scr = Screen()
    width, height=500,400
    setup(scr, width, height)

    colors=["red", "orange", "yellow", "green", "blue", "purple"]
    user_resp = None
    user_resp = scr.textinput("Choose Turtle", f"Please choose the turtle you think will win from colors {colors}. what color do you choose?")
    print(f"user chose turtle {user_resp}")

    turtles = setup_game(colors)
    winner = start_race(turtles, user_resp, width, height)
    print(f"Race is over. Winner is {colors[winner]} turtle")
    if colors[winner] == user_resp.lower():
        print("You are guessed the winner!!")

    #t.pendown()
    scr.listen()
    #scr.onkey(fun=partial(clear_screen, t), key="c" )

    scr.exitonclick()

if __name__ == "__main__":
    main()



