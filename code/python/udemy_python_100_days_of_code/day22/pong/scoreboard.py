from turtle import Turtle
from pongScreen import PongScreen

class Scoreboard(Turtle):
    def __init__(self, pong_screen: PongScreen, shape: str = "classic", undobuffersize: int = 1000, visible: bool = True) -> None:
        super().__init__(shape, undobuffersize, visible)
        self.color("white")
        self.penup()
        self.hideturtle()
        self.l_score = 0
        self.r_score = 0
        self.pong_screen = pong_screen
        self.refresh_score()

    def refresh_score(self):
        self.clear()
        self._show_left_score() 
        self._show_right_score() 

    def inc_r_score(self) -> None:
        self.r_score += 1
        self.refresh_score()

    def inc_l_score(self) -> None:
        self.l_score += 1
        self.refresh_score()

    def _show_left_score(self):
        self.goto(-(self.pong_screen.width/8), self.pong_screen.height/3)
        self.write(self.l_score, align="center", font=("courier", 80, "normal"))

    def _show_right_score(self):
        self.goto(+(self.pong_screen.width/8), self.pong_screen.height/3)
        self.write(self.r_score, align="center", font=("courier", 80, "normal"))