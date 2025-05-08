from turtle import Turtle

class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.color("white")
        self.penup()
        self.goto(0, 0)  # Ball starts at the center
        self.x_move = 6  # Slower initial speed
        self.y_move = 6  # Slower initial speed
        self.move_speed = 0.2  # Slower speed for initial movement
        self.hit_counter = 0  # Counter to track the number of hits

    def move(self):
        new_x = self.xcor() + self.x_move
        new_y = self.ycor() + self.y_move
        self.goto(new_x, new_y)

    def bounce_y(self):
        self.y_move *= -1
        self.hit_counter += 1  # Increment hit counter after every hit

    def bounce_x(self):
        self.x_move *= -1
        self.hit_counter += 1  # Increment hit counter after every hit
        if self.hit_counter >= 3:  # Speed up after every 3 hits
            self.move_speed *= 1.05  # Increase speed
            self.hit_counter = 0  # Reset hit counter after increasing speed

    def reset_position(self):
        self.goto(0, 0)
        self.move_speed = 0.2  # Reset to the initial slower speed
        self.x_move = 6  # Reset ball's speed on X-axis
        self.y_move = 6  # Reset ball's speed on Y-axis
        self.hit_counter = 0  # Reset hit counter
        self.bounce_x()  # Ensure the ball bounces when reset
