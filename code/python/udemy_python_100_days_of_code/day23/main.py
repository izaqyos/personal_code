#!/opt/homebrew/bin/python3

import time
from turtle import Screen
from player import Player
from car_manager import CarManager
from scoreboard import Scoreboard
from gameover import Gameover
import logging

logging.basicConfig(level=logging.DEBUG, filename='turtle_crossing_game.log', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("TurtleCrossingLogger")
logger.info("Initializing...")
screen = Screen()
screen.setup(width=600, height=600)
screen.tracer(0)

game_is_on = True
player_t = Player(logger, screen)
car_mgr = CarManager(logger, screen)
scoreboard = Scoreboard(logger, screen)
gameover = Gameover(logger, screen)

SLEEP_TIME = 0.1
GEN_CAR_BATCH_FREQUENCY = 1 # in seconds
INITIAL_NUM_CARS = 1
num_cars = INITIAL_NUM_CARS
iteration_num = 0

car_mgr.generate_cars(num_cars)
while game_is_on:
    scoreboard.refresh_level()
    # This is a method of throtteling car generation. otherwise we have 10 car generated per second...
    #iteration_num+=1
    #if iteration_num % (GEN_CAR_BATCH_FREQUENCY/0.1) == 0:
    #    logger.debug(f"Generating {num_cars} new cars")
    #    car_mgr.generate_cars(num_cars)
    #    #num_cars+=1

    #Another method of throtteling is using the generate_cars_chance() method which randomely creates cars
    car_mgr.generate_cars_chance(1)

    time.sleep(0.1)
    car_mgr.move_cars()
    if car_mgr.detect_collision(player_t):
        game_is_on = False
        gameover.show_msg()

    if  player_t.has_reached_end():
        car_mgr.level_up()
        scoreboard.inc_level()
        player_t.go_to_start()

    screen.update()

screen.exitonclick() #keep screen open until user clicks
