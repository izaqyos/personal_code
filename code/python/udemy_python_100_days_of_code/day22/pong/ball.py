from turtle import Turtle
class Ball(Turtle):

    """Pong Game ball. """

    def __init__(self, logger, x_pos=0, y_pos=0, width=1, height=1):
        super().__init__()
        self.logger = logger
        self.logger.info("Ball created")
        self.shape("circle")
        self.ht() 
        self.color("white")
        self.shapesize(stretch_wid=height, stretch_len=width)
        self.penup()
        self.goto(x_pos,y_pos)
        self.st()
        self.y_axis_direction = 1
        self.x_axis_direction = 1
        #move_angle=37
        #self.left(move_angle)

    def bounce(self, move_distance=5, axis=0): #axis 0 -> bounce on y axis, axis 1 -> bounce on x axis
        if axis:
            self.x_axis_direction *= -1
        else:
            self.y_axis_direction *= -1

    def move(self, move_distance=10):
        #self.fd(move_distance)
        x,y = self.pos()
        self.logger.info(f"Ball::move() called. move_distance={move_distance}, y_axis_direction={self.y_axis_direction}, x_axis_direction={self.x_axis_direction}, goto={(x+move_distance*self.x_axis_direction, y+move_distance*self.y_axis_direction)}")
        self.goto(x+move_distance*self.x_axis_direction, y+move_distance*self.y_axis_direction)

    def reposition_in_center(self):
        self.goto(0,0)
        self.x_axis_direction *= -1
        self.y_axis_direction *= -1


        
