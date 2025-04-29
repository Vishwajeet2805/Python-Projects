from turtle import Turtle, Screen

pen_color = input("Enter pen color (e.g. red, blue): ").lower()
bg_color = input("Enter background color: ").lower()
pen_thickness = int(input("Enter pen thickness (e.g. 1 to 10): "))
tim = Turtle()
tim.color(pen_color)
tim.pensize(pen_thickness)
screen = Screen()
screen.bgcolor(bg_color)

def move_forwards():
    tim.forward(15)

def move_backwards():
    tim.backward(15)

def turn_left():
    tim.setheading(tim.heading() + 15)

def turn_right():
    tim.setheading(tim.heading() - 15)

def clear():
    tim.clear()
    tim.penup()
    tim.home()
    tim.pendown()

screen.listen()
screen.onkey(move_forwards, "w")
screen.onkey(move_backwards, "s")
screen.onkey(turn_left, "a")
screen.onkey(turn_right, "d")
screen.onkey(clear, "c")

screen.exitonclick()
