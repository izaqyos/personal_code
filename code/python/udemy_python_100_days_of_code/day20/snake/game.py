#!/opt/homebrew/bin/python3

from turtle import Screen
from snake import Snake
from food import Food
from scoreboard import Scoreboard
import time

import pdb
class Game:
    def __init__(self):
        print("Game: CTOR() called")
        self.screen = Screen()
        self.screen.setup(width=600, height=600)
        self.screen.bgcolor("black")
        self.screen.title("Snake Game")
        self.screen.tracer(0)  # update screen only after update is called
        self.snake = Snake()
        self.food = Food()
        self.scoreboard = Scoreboard()
        self._listen()
        self.game_on = False

    def _listen(self):
        self.screen.listen()
        self.screen.onkey(self.snake.up, "Up")
        self.screen.onkey(self.snake.down, "Down")
        self.screen.onkey(self.snake.left, "Left")
        self.screen.onkey(self.snake.right, "Right")

    def _is_tail_collision(self):
        head = self.snake.get_head()
        #print(f"_is_tail_collision(), length={len(self.snake.get_segments())}")
        for t in self.snake.get_segments():
            #print(f"segment detected at {t.xcor()},{t.ycor()}")
            pass
        for t in self.snake.get_segments()[1:]:
            #print(f"head detected at {self.snake.get_head().xcor()},{self.snake.get_head().ycor()}, segment detected at {t.xcor()},{t.ycor()}")
            if t.distance(head)<10:
                return True
        #for t in self.snake.get_segments():
        #    if t == head or t == self.snake.get_segments()[1]:
        #        pass
        #    elif t.distance(head)<10:
        #        return True
        return False

    def _is_collision(self):
        #print(f"_is_collision(): head location: {self.snake.get_head().pos()}, food location: {self.food.pos()}, distance: {self.snake.get_head().distance(self.food) }")
        return self.snake.get_head().distance(self.food) < 14 #food 10X10, snake head 20X20 - 14 pixels is close enough to consider it a collision

    def _hit_wall(self):
        return self.snake.get_head().xcor() > 290 or self.snake.get_head().xcor() < -290 or self.snake.get_head().ycor() > 290 or self.snake.get_head().ycor() < -290

    def start_game(self):
        print("Game: start_game() called")
        #pdb.set_trace()
        self.game_on = True
        self.scoreboard.writeText()
        while self.game_on:
            self.screen.update()
            time.sleep(0.1)
            self.snake.move()
            if self._is_collision():
                self.scoreboard.updateScore(1)
                self.scoreboard.writeText()
                self.food.refresh()
                self.snake.extend()

            if self._hit_wall():
                print(f"Wall hit detected at {self.snake.get_head().xcor()},{self.snake.get_head().ycor()}")
                self.end_game()
            if self._is_tail_collision():
                print(f"collision with tail detected at {self.snake.get_head().xcor()},{self.snake.get_head().ycor()}")
                self.end_game()

        self.screen.exitonclick()

    def end_game(self):
        #self.game_on = False
        self.scoreboard.gameOverMsg()
        self.scoreboard.reset()
        self.snake.reset()
        self.scoreboard.writeText()
