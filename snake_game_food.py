from turtle import Turtle
import random

class Food(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.penup()
        self.shapesize(0.5, 0.5)
        self.speed("fastest")
        self.refresh()

    def refresh(self):
        random_color = (random.random(), random.random(), random.random())
        self.color(random_color)
        x = random.randint(-280, 280)
        y = random.randint(-280, 280)
        self.goto(x, y)
