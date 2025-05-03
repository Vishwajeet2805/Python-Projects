from turtle import Screen
from snake import Snake
from food import Food
from scoreboard import Scoreboard
import time

# Setup
screen = Screen()
screen.setup(600, 600)
screen.bgcolor("black")
screen.title("Snake Game")
screen.tracer(0)
screen.colormode(1.0)

snake, food, scoreboard = Snake(), Food(), Scoreboard()
screen.listen()

# Direct key bindings
screen.onkey(snake.up, "Up")
screen.onkey(snake.down, "Down")
screen.onkey(snake.left, "Left")
screen.onkey(snake.right, "Right")

# Game loop
game_is_on, speed = True, 0.075
while game_is_on:
    screen.update()
    time.sleep(speed)
    snake.move()

    # Collision with food
    if snake.head.distance(food) < 15:
        food.refresh()
        snake.extend()
        scoreboard.increase_score()
        if scoreboard.score % 5 == 0:
            speed *= 0.9
            scoreboard.level_up()

    # Wall collision
    x, y = snake.head.xcor(), snake.head.ycor()
    if x > 280 or x < -280 or y > 280 or y < -280:
        screen.bgcolor("red")
        scoreboard.game_over()
        game_is_on = False

    # Tail collision (no any())
    for segment in snake.segments[1:]:
        if snake.head.distance(segment) < 10:
            screen.bgcolor("red")
            scoreboard.game_over()
            game_is_on = False
            break

screen.exitonclick()