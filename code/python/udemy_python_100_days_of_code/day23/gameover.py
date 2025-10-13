from turtle import Turtle
FONT = ("Courier", 24, "normal")

class Gameover(Turtle):
    def __init__(self, logger, screen, shape: str = "classic", undobuffersize: int = 1000, visible: bool = True) -> None:
        super().__init__(shape, undobuffersize, visible)
        self.color("red")
        self.penup()
        self.hideturtle()
        self.gameover_msg = "Game Over"
        self.screen = screen

    def show_msg(self):
        self.clear()
        self.goto(-30, 0)
        self.write(self.gameover_msg, align="center", font=FONT)

