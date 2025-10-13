#!/opt/homebrew/bin/python3
from pongGame import PongGame
from pongScreen import PongScreen 
from ball import Ball
from paddle import Paddle
from turtle import Turtle, Screen
from scoreboard import Scoreboard
import logging


def register_paddle_keys(screen, right_paddle, left_paddle):
    screen.listen()
    screen.onkey(right_paddle.goup, "Up")
    screen.onkey(right_paddle.godown, "Down")
    screen.onkey(left_paddle.goup, "w")
    screen.onkey(left_paddle.godown, "s")

def main():
    logging.basicConfig(level=logging.DEBUG, filename='pong_game.log', format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger("PongGameLogger")
    logger.info("Initializing...")
    screen = Screen()
    pong_screen = PongScreen(logger, screen)
    ball = Ball(logger)
    scoreboard = Scoreboard(pong_screen)

    right_paddle = Paddle(logger, 350, 0)
    left_paddle = Paddle(logger, -350, 0)
    game = PongGame(logger, pong_screen, ball, left_paddle, right_paddle, scoreboard)
    register_paddle_keys(screen, right_paddle, left_paddle)
    game.start_game()

    #screen = Screen()
    #screen.bgcolor("black")
    #screen.setup(width=800, height=600)
    #screen.title("pong")
    #player_paddle = Paddle(screen)

    #paddle = Turtle(shape="square")
    ##paddle.shape("square")
    #paddle.color("white")
    #paddle.shapesize(stretch_wid=5, stretch_len=1)
    #screen.exitonclick()
    screen.exitonclick()


if __name__ == "__main__":
    main()
