from turtle import Turtle, Screen, colormode, speed, pensize
import random

tim = [Turtle(), colormode(255), speed("fastest"), pensize(3)]
screen = Screen()
screen.bgcolor("black")

def glowing_colour():
    neon_colors = [
        (255, 0, 255), (0, 255, 255), (255, 255, 0), (0, 255, 0),
        (255, 105, 180), (0, 191, 255), (255, 165, 0), (127, 255, 0),
        (0, 250, 154), (138, 43, 226)]
    return random.choice(neon_colors)

def draw_pattern(pattern_type):
    if pattern_type == 'spirograph':
        gap = 5
        for _ in range(int(360 / gap)):
            tim[0].color(glowing_colour())
            tim[0].circle(100)
            tim[0].setheading(tim[0].heading() + gap)
    elif pattern_type == 'star':
        for _ in range(50):
            tim[0].color(glowing_colour())
            for _ in range(5):
                tim[0].forward(100)
                tim[0].right(144)
            tim[0].right(10)
    elif pattern_type == 'square_spiral':
        length = 5
        for _ in range(100):
            tim[0].color(glowing_colour())
            tim[0].forward(length)
            tim[0].right(90)
            length += 5
    elif pattern_type == 'hexagon_web':
        for _ in range(36):
            tim[0].color(glowing_colour())
            for _ in range(6):
                tim[0].forward(100)
                tim[0].right(60)
            tim[0].right(10)
    elif pattern_type == 'triangle_spiral':
        length = 5
        for _ in range(120):
            tim[0].color(glowing_colour())
            tim[0].forward(length)
            tim[0].right(120)
            length += 3
    elif pattern_type == 'dots_grid':
        tim[0].penup()
        tim[0].setpos(-200, -200)
        for y in range(10):
            for x in range(10):
                tim[0].dot(20, glowing_colour())
                tim[0].forward(40)
            tim[0].setheading(90)
            tim[0].forward(40)
            tim[0].setheading(180)
            tim[0].forward(400)
            tim[0].setheading(0)
    elif pattern_type == 'mandala':
        for _ in range(36):
            tim[0].color(glowing_colour())
            for _ in range(6):
                tim[0].circle(50)
                tim[0].left(60)
            tim[0].right(10)
    elif pattern_type == 'spiral_galaxy':
        distance, angle = 1, 10
        for i in range(300):
            tim[0].color(glowing_colour())
            tim[0].forward(distance)
            tim[0].left(angle)
            distance += 0.2
            angle += 0.05
    elif pattern_type == 'radiating_lines':
        for _ in range(72):
            tim[0].color(glowing_colour())
            tim[0].forward(150)
            tim[0].backward(150)
            tim[0].right(5)

choice = screen.textinput("Shape Selector",
    "1 - Spirograph Flower \n2 - Star Pattern \n3 - Square Spiral \n4 - Hexagon Web \n"
    "5 - Triangle Spiral \n6 - Colorful Dots Grid \n7 - Mandala Circles \n8 - Spiral Galaxy \n9 - Radiating Lines\n"
    "Enter a number (1 to 9):")

patterns = {'1': 'spirograph', '2': 'star', '3': 'square_spiral', '4': 'hexagon_web',
            '5': 'triangle_spiral', '6': 'dots_grid', '7': 'mandala', '8': 'spiral_galaxy', '9': 'radiating_lines'}

draw_pattern(patterns.get(choice, ''))
screen.exitonclick()
