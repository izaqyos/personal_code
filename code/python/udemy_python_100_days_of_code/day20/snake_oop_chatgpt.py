#!/opt/homebrew/bin/python3

import turtle
import time
import random


class SnakeGame:
    def __init__(self):
        self.window = turtle.Screen()
        self.window.title("Snake Game")
        self.window.bgcolor("black")
        self.window.setup(width=600, height=600)
        self.window.tracer(0)

        self.snake = Snake()
        self.food = Food()

        self.window.listen()
        self.window.onkey(self.snake.move_up, "Up")
        self.window.onkey(self.snake.move_down, "Down")
        self.window.onkey(self.snake.move_left, "Left")
        self.window.onkey(self.snake.move_right, "Right")

        self.game_over = False

    def play(self):
        while not self.game_over:
            self.window.update()
            self.snake.move()

            if self.snake.head.distance(self.food) < 20:
                self.snake.extend()
                self.food.refresh()

            if self.snake.head.xcor() > 290 or self.snake.head.xcor() < -290 or self.snake.head.ycor() > 290 or self.snake.head.ycor() < -290:
                self.game_over = True

            for segment in self.snake.segments[1:]:
                if self.snake.head.distance(segment) < 10:
                    self.game_over = True

            time.sleep(0.1)

        self.window.bye()


class Snake:
    def __init__(self):
        self.segments = []
        self.create_snake()
        self.head = self.segments[0]

    def create_snake(self):
        for i in range(3):
            segment = turtle.Turtle()
            segment.shape("square")
            segment.color("white")
            segment.penup()
            segment.goto(-i * 20, 0)
            self.segments.append(segment)

    def move(self):
        for i in range(len(self.segments) - 1, 0, -1):
            x = self.segments[i - 1].xcor()
            y = self.segments[i - 1].ycor()
            self.segments[i].goto(x, y)

        self.head.forward(20)

    def move_up(self):
        if self.head.heading() != 270:
            self.head.setheading(90)

    def move_down(self):
        if self.head.heading() != 90:
            self.head.setheading(270)

    def move_left(self):
        if self.head.heading() != 0:
            self.head.setheading(180)

    def move_right(self):
        if self.head.heading() != 180:
            self.head.setheading(0)

    def extend(self):
        segment = turtle.Turtle()
        segment.shape("square")
        segment.color("white")
        segment.penup()
        self.segments.append(segment)

    def reset(self):
        for segment in self.segments:
            segment.goto(1000, 1000)
        self.segments.clear()
        self.create_snake()
        self.head = self.segments[0]


class Food(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.color("red")
        self.penup()
        self.refresh()

    def refresh(self):
        x = random.randint(-280, 280)
        y = random.randint(-280, 280)
        self.goto(x, y)


# Unit Test
def test_snake_move_up():
    game = SnakeGame()
    game.snake.move_up()
    assert game.snake.head.heading() == 90


def test_snake_move_down():
    game = SnakeGame()
    game.snake.move_down()
    assert game.snake.head.heading() == 270


def test_snake_move_left():
    game = SnakeGame()
    game.snake.move_left()
    assert game.snake.head.heading() == 180


def test_snake_move_right():
    game = SnakeGame()
    game.snake.move_right()
    assert game.snake.head.heading() == 0


if __name__ == "__main__":
    test_snake_move_up()
    test_snake_move_down()
    test_snake_move_left()
    test_snake_move_right()
    print("All tests pass.")

    game = SnakeGame()
    game.play()

