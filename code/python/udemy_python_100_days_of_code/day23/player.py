from turtle import Turtle

STARTING_POSITION = (0, -280)
MOVE_DISTANCE = 10
FINISH_LINE_Y = 280


class Player(Turtle):
    def __init__(self, logger, screen):
        super().__init__()
        self.logger = logger
        self.logger.info(f"Initializing player")
        self.screen = screen
        self.ht() 
        self.shape("turtle")
        self.seth(90)
        self.penup()
        self.go_to_start()
        self.st()
        self.screen.listen()
        self.screen.onkey(self._move, "Up")

    def _move(self):
        #self.logger.debug(f"Player::_move called - moving to {self.xcor()},{self.ycor()+10}")
        #self.goto(self.xcor(),self.ycor()+MOVE_DISTANCE)
        #self.logger.debug(f"Player::_move called - moving forward {MOVE_DISTANCE} distance")
        self.forward(MOVE_DISTANCE)

    def go_to_start(self):
        self.goto(STARTING_POSITION)

    def has_reached_end(self):
        if self.ycor() > FINISH_LINE_Y:
            self.logger.info("Player has reached the other side")
            return True
        else:
            return False
