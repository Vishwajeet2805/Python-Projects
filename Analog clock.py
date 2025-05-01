import turtle, time

window = turtle.Screen()
window.bgcolor("black")
pen = [turtle.Turtle()][0]; pen.speed(0); pen.pensize(3); pen.hideturtle()

def draw_clock(hour, minute, second):
    pen.clear()
    pen.penup()
    pen.goto(0, 0)
    pen.setheading(90)
    pen.color("white")
    for _ in range(12):
        pen.forward(180)
        pen.pendown()
        pen.forward(20)
        pen.penup()
        pen.goto(0, 0)
        pen.right(30)

    pen.penup()
    pen.goto(0, 0)
    pen.setheading(60)
    pen.color("white")
    for number in range(1, 13):
        pen.penup()
        pen.forward(150)
        pen.pendown()
        pen.write(str(number), align="center", font=("Arial", 18, "normal"))
        pen.penup()
        pen.backward(150)
        pen.right(30)

    pen.penup()
    pen.goto(0, 0)
    pen.setheading(90)
    pen.color("gold")
    angle = (hour * 30) + (minute * 0.5)
    pen.right(angle)
    pen.pendown()
    pen.forward(100)

    pen.penup()
    pen.goto(0, 0)
    pen.setheading(90)
    pen.color("cyan")
    angle = (minute * 6) + (second * 0.1)
    pen.right(angle)
    pen.pendown()
    pen.forward(150)

    pen.penup()
    pen.goto(0, 0)
    pen.setheading(90)
    pen.color("red")
    angle = second * 6
    pen.right(angle)
    pen.pendown()
    pen.forward(180)

def update_clock(hour, minute, second):
    while True:
        draw_clock(hour % 12, minute, second)
        window.update()
        time.sleep(1)
        second += 1
        if second == 60:
            second = 0
            minute += 1
        if minute == 60:
            minute = 0
            hour += 1
        if hour == 24:
            hour = 0

hour = int(input("Enter the hour (0-23): "))
minute = int(input("Enter the minute (0-59): "))
second = int(input("Enter the second (0-59): "))

window.tracer(0)
update_clock(hour, minute, second)
turtle.mainloop()
