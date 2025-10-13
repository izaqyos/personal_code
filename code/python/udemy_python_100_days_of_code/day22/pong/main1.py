#!/opt/homebrew/bin/python3
from turtle import Turtle, Screen

screen = Screen()
screen.bgcolor("black")
screen.setup(width=800, height=600)
screen.title("pong")

paddle = Turtle(shape="square")
#paddle.shape("square")
paddle.color("white")
paddle.shapesize(stretch_wid=5, stretch_len=1)

screen.exitonclick()
