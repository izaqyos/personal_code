from turtle import Turtle

class Paddle(Turtle):
    def __init__(self, logger, screen, x_pos=350, y_pos=0, move_length=20):
        super().__init__()
        self.logger = logger
        self.logger.info(f"paddle created at position {x_pos},{y_pos}")
        self.screen = screen
        self.move_length = move_length
        #self.paddle = Turtle(shape="square")
        self.shape("square")
        self.ht() 
        self.color("white")
        self.shapesize(stretch_wid=5, stretch_len=1)
        self.penup()
        self.goto(x_pos,y_pos)
        self.st()

    def godown(self):
        self.logger.debug(f"Paddle::godown() called")
        x,y = self.pos()
        self.setpos(x, y-self.move_length)

    def goup(self):
        self.logger.debug(f"Paddle::goup() called")
        x,y = self.pos()
        self.setpos(x, y+self.move_length)

    def _listen(self):
        self.logger.debug(f"Paddle::_listen() called")
        
class LeftPaddle(Paddle):
    def __init__(self, logger, screen):
        super().__init__(logger, screen, x_pos=350, y_pos=0, move_length=20)
        self._listen()

    def _listen(self):
        self.logger.debug(f"LeftPaddle::_listen() called")
        self.screen.listen()
        self.screen.onkey(self.goup, "Up")
        self.screen.onkey(self.godown, "Down")
        
class RightPaddle(Paddle):
    def __init__(self, logger, screen):
        super().__init__(logger, screen, x_pos=-350, y_pos=0, move_length=20)
        self._listen()

    def _listen(self):
        self.logger.debug(f"RightPaddle::_listen() called")
        self.screen.listen()
        self.screen.onkey(self.goup, "w")
        self.screen.onkey(self.godown, "s")

