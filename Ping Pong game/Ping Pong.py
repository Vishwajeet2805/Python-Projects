from turtle import Screen
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard
from center_line import CenterLine

# Setup screen
screen = Screen()
screen.bgcolor("black")
screen.setup(width=800, height=600)
screen.title("Ping Pong")
screen.tracer(0)  # Disable automatic screen updates to manually update

# Ask user for score limit
score_limit = int(screen.numinput("Set Score Limit", "Enter the score to end the game:") or 5)

# Create game objects
r_paddle = Paddle((350, 0))  # Right paddle at (350, 0)
l_paddle = Paddle((-350, 0))  # Left paddle at (-350, 0)
ball = Ball()  # Ball starts at (0, 0)
scoreboard = Scoreboard()
CenterLine()  # Center line for the game

# Controls
screen.listen()
screen.onkey(r_paddle.go_up, "Up")
screen.onkey(r_paddle.go_down, "Down")
screen.onkey(l_paddle.go_up, "w")
screen.onkey(l_paddle.go_down, "s")

# Check if there's a winner
def check_for_winner():
    if scoreboard.l_score >= score_limit:
        scoreboard.clear()
        scoreboard.goto(0, 0)
        scoreboard.write(f"Left Player Wins!", align="center", font=("Courier", 24, "normal"))
        return True
    elif scoreboard.r_score >= score_limit:
        scoreboard.clear()
        scoreboard.goto(0, 0)
        scoreboard.write(f"Right Player Wins!", align="center", font=("Courier", 24, "normal"))
        return True
    return False

# Main game loop
def game_loop():
    ball.move()

    # Check for wall collision
    if ball.ycor() > 280 or ball.ycor() < -280:
        ball.bounce_y()

    # Check for paddle collision
    if (ball.distance(r_paddle) < 50 and ball.xcor() > 320) or (ball.distance(l_paddle) < 50 and ball.xcor() < -320):
        ball.bounce_x()

    # Check if ball goes out of bounds
    if ball.xcor() > 380:
        ball.reset_position()
        scoreboard.l_point()

    if ball.xcor() < -380:
        ball.reset_position()
        scoreboard.r_point()

    # Check for winner
    if check_for_winner():
        return

    screen.update()  # Manually update the screen
    screen.ontimer(game_loop, 20)  # Repeat the game loop

# Start the game loop
game_loop()

# Keep the window open
screen.mainloop()
