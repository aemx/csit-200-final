import turtle as t
from time import sleep
import random

# Set up global variables
sw, sh = 1280, 720
key_down = "Down"
key_up = "Up"

# Turn off drawing animations
t.tracer(0, 0)

# Initialize the game's window
window = t.Screen()
window.title("Pong")
window.setup(width=sw, height=sh)
window.bgcolor("black")

"""
Function that clamps a value at a minimum and maximum.
"""
clamp = lambda num, lo, hi : min(max(lo, num), hi)

"""
The default range function adjusted for floating-point values.
"""
range_float = lambda lo, hi, step=1 : range(int(lo), int(hi), step)

"""
A function to generate a square or rectangle on the screen.
"""
def make_shape(color, length, width, xpos, ypos):
    shape = t.Turtle()
    shape.speed(0)
    shape.shape("square")
    shape.color(color)
    shape.shapesize(length, width)
    shape.up()
    shape.goto(xpos, ypos)
    return shape

"""
Function to create a paddle, defined by player number and color.
"""
def paddle(pn, color):
    paddle = make_shape(color, 5, 1, -(pn % 2 * 2 - 1) * sw/2.35, 0)
    paddle.velocity = 0
    return paddle

# Set up paddles
player = paddle(1, "#4b8bbe")
opponent = paddle(2, "#ffe873")
opponent.hitpos = random.random()

# Player control
# player_stop_up/down prevents stutter when both keys are pressed.
def player_up(): player.velocity = 1
def player_down(): player.velocity = -1
def player_stop_up():
    if player.velocity == 1: player.velocity = 0
def player_stop_down():
    if player.velocity == -1: player.velocity = 0

# Keyboard binding
window.onkeypress(player_up, key_up)
window.onkeypress(player_down, key_down)
window.onkeyrelease(player_stop_up, key_up)
window.onkeyrelease(player_stop_down, key_down)
window.listen()

# Set up divider
for i in range_float(-sh/1.5, sh/1.5, 60):
    divider = make_shape("grey", 2, 0.7, 0, i)

# Set up ball
ball = make_shape("white", 0.7, 0.7, 0, 0)
ball.velocity_x, ball.velocity_y = -1, 1

# Update loop
while True:
    # Player movement
    player.sety(clamp(player.ycor() + player.velocity*8, (-sh/2)+60, (sh/2)-60))

    # Opponent movement
    opponent.sety(clamp(ball.ycor() + 75 * opponent.hitpos, (-sh/2)+60, (sh/2)-60))

    # Ball movement
    ball.velocity_y *= -1 if abs(ball.ycor()) >= (sh/2)-16 else 1
    ball.goto(ball.xcor() + ball.velocity_x*8, ball.ycor() + ball.velocity_y*8)

    # Paddle collision logic for player
    # Also, generate a new position for the opponent to follow
    if ball.xcor() in range_float(-sw/2.35+5, -sw/2.35+20) and \
    ball.ycor() in range_float(player.ycor()-62,(player.ycor()+62)):
        ball.velocity_x *= -1
        opponent.hitpos = random.random()

    # Paddle collision logic for opponent
    ball.velocity_x *= -1 if ball.xcor() in range_float(sw/2.35-20, sw/2.35-5) and \
    ball.ycor() in range_float(opponent.ycor()-62,(opponent.ycor()+62)) else 1

    # If the ball crosses the threshold, reset everything
    if abs(ball.xcor()) >= (sw/2.1):
        player.sety(0)
        ball.goto(0,0)

    # Update the window
    window.update()
    sleep(1/60)