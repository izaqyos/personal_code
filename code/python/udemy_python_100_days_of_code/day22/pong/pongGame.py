#!/opt/homebrew/bin/python3

import time


class PongGame:
    def __init__(self, logger, pong_screen, ball, left_paddle, right_paddle, scoreboard):
        self.logger = logger
        self.logger.info("PongGame Initializing")
        self.pong_screen = pong_screen
        self.game_on = False
        self.ball = ball
        self.scoreboard = scoreboard
        self.left_paddle = left_paddle
        self.right_paddle = right_paddle
        self.move_speed = 0.05

    def end_game(self):
        self.game_on = False

    def start_game(self):
        self.game_on = True
        while self.game_on:
            self.ball.move()
            if self.pong_screen.is_colision(self.ball.ycor()):
                self.logger.info(
                    f"PongGame::start_game() - Detected colision. Ball pos is {self.ball.pos()}")
                self.ball.bounce()
            if self.is_colision_with_paddles():
                self.logger.info(
                    f"PongGame::start_game() - Detected colision with paddle")
                self.ball.bounce(axis=1)
                self._increase_ball_speed()

            if self.is_ball_out_of_screen():
                self.logger.info("Detected ball out of bounds")
                self.update_score()
                self.ball.reposition_in_center()

            # refresh screen manually since we turned off tracer
            self.pong_screen.update_screen()
            self._set_speed(self.move_speed)

    def _increase_ball_speed(self):
        self.move_speed /= 1.1

    def _set_speed(self, rate):
        """
        method changes refresh rate actually. But from game perspective it controlls ball speed.
        """
        time.sleep(rate)

    def update_score(self): 
        self.logger.info("updating score")
        if self.ball.xcor() < self.pong_screen.width/-2: #left misses, right gains point
            self.scoreboard.inc_r_score()
        if (self.ball.xcor() > self.pong_screen.width/2):
            self.scoreboard.inc_l_score()

    def is_ball_out_of_screen(self): #ToDo, for score tracking separate the condition to left (-400) and right (400) players:
        return (self.ball.xcor() < self.pong_screen.width/-2) or (self.ball.xcor() > self.pong_screen.width/2)

    def is_colision_with_paddles(self, collision_margin=20):
        # self.logger.info(f"PongGame::is_colision_with_paddles() called")
        return ((self.ball.distance(self.left_paddle) < 50 and (self.ball.xcor() < self.left_paddle.x_pos + collision_margin))
                or ((self.ball.distance(self.right_paddle) < 50 and self.ball.xcor() > self.right_paddle.x_pos-collision_margin))
                )
