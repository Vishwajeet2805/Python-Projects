from turtle import Turtle

class CenterLine(Turtle):

    def __init__(self):
        super().__init__()
        self.color("white")
        self.penup()
        self.hideturtle()
        self.goto(0, 300)
        self.setheading(270)  # Point downwards
        self.draw_dashed_line()

    def draw_dashed_line(self):
        for _ in range(30):
            self.pendown()
            self.forward(10)
            self.penup()
            self.forward(10)
