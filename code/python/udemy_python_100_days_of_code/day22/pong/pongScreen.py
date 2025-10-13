from turtle import Screen

class PongScreen:
    def __init__(self, logger, screen):
        self.logger = logger
        self.logger.info("Screen CTOR called")
        self._screen = screen
        self._width = 800
        self._height = 600
        self._screen.setup(self.width, self.height)
        self._screen.bgcolor("black")
        self._screen.title("Pong Game")
        self._screen.tracer(0)  # update screen only after update is called

    def __del__(self):
        self.logger.info("Screen DTOR called")
        #self._screen.exitonclick()

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def screen(self):
        return self._screen

    def update_screen(self):
        self.screen.update()

    def is_colision(self, y_cor, collision_margin=20):
        # return ( (x_cor > self.width/2 -10) or (x_cor < -self.width/2 +10) or (y_cor > self.height/2 -10) or (y_cor < -self.height/2 +20) )  
        return   (y_cor > self.height/2 -collision_margin) or (y_cor < -self.height/2 +collision_margin)

    

