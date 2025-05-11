from turtle import Turtle
import random

COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]
STARTING_MOVE_DISTANCE = 5
MOVE_INCREMENT = 10


class CarManager:

    def __init__(self):
        self.all_cars = []
        self.car_speed = STARTING_MOVE_DISTANCE
        self.level = 1  # Track the level

    def create_car(self):
        # Adjust car creation chance based on level
        creation_chance = max(1, 6 - self.car_speed // MOVE_INCREMENT)

        # Increase the number of cars after level 1
        if self.level > 1:
            creation_chance = max(1, 4 - self.car_speed // MOVE_INCREMENT)  # More cars spawn

        if random.randint(1, creation_chance) == 1:
            new_car = Turtle("square")
            new_car.shapesize(stretch_wid=1, stretch_len=2)
            new_car.penup()
            new_car.color(random.choice(COLORS))
            random_y = random.randint(-250, 250)  # Random position within screen height
            new_car.goto(300, random_y)
            self.all_cars.append(new_car)

    def move_cars(self):
        for car in self.all_cars:
            car.backward(self.car_speed)

    def level_up(self):
        self.car_speed += MOVE_INCREMENT
        self.level += 1  # Increase level
