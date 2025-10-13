from turtle import Turtle
FONT = ("Courier", 24, "normal")

class Scoreboard(Turtle):
    def __init__(self, logger, screen, shape: str = "classic", undobuffersize: int = 1000, visible: bool = True) -> None:
        super().__init__(shape, undobuffersize, visible)
        self.color("blue")
        self.penup()
        self.hideturtle()
        self.level = 1
        self.level_prefix = "Level : "
        self.screen = screen
        self.refresh_level()

    def refresh_level(self):
        self.clear()
        self._show_level() 

    def inc_level(self) -> None:
        self.level += 1
        self.refresh_level()

    def _show_level(self):
        self.goto(-220, 260)
        self.write(self.level_prefix+str(self.level), align="center", font=FONT)

