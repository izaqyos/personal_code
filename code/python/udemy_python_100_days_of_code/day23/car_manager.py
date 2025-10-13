from car import Car
from random import randint, choice

COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]
STARTING_MOVE_DISTANCE = 5
MOVE_INCREMENT = 10
INITIAL_RANDOM_CHANCE_CREATE_CAR = 6 #denominator, e.g. 1/6 chance


class CarManager:
    def __init__(self, logger, screen):
        self.logger = logger
        self.screen = screen
        self.logger.info(f"Initializing CarManager")
        self.batch_num = 0
        self.cars = [] 

    def generate_cars_chance(self, num_cars):
        #decide how many cars to generate. colors and positions are set randomly. each batch increase move distance by move increment
        chance = randint(1, INITIAL_RANDOM_CHANCE_CREATE_CAR)
        if chance == 6:
            for i in range(num_cars):
                self.logger.debug(f"CarManager::generate_cars() - generating car {i+1}/{num_cars}")
                self.cars.append(Car(self.logger, self.screen, choice(COLORS), STARTING_MOVE_DISTANCE, MOVE_INCREMENT))
            self.batch_num +=1

    def generate_cars(self, num_cars):
        #decide how many cars to generate. colors and positions are set randomly. each batch increase move distance by move increment
        for i in range(num_cars):
            self.logger.debug(f"CarManager::generate_cars() - generating car {i+1}/{num_cars}")
            self.cars.append(Car(self.logger, self.screen, choice(COLORS), STARTING_MOVE_DISTANCE, MOVE_INCREMENT))
        self.batch_num +=1

    def level_up(self):
        """
        increase cars speed
        """
        self.logger.debug(f"CarManager::level_up() called, increasing cars speed to {self.cars[0].get_speed()+MOVE_INCREMENT}")
        for car in self.cars:
            cur_speed = car.get_speed()
            car.set_speed(cur_speed+MOVE_INCREMENT)

    def move_cars(self):
        #self.logger.debug(f"CarManager::move_cars() - moving cars")
        for i,car in enumerate(self.cars):
            car.move()
            if car.xcor() < -330:
                self.logger.debug(f"Car index {i} is out of screen. deleting it..")
                self._delete_car(i)

    def detect_collision(self, aturtle):
        for car in self.cars:
            if aturtle.distance(car) < 20:
                self.logger.debug(f"Detected collision with a car")
                return True
        return False


    def _delete_car(self, car_index):
        del self.cars[car_index]

