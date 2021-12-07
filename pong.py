import turtle as t

# Set up global variables
sw, sh = 1280, 720
key_down = "Down"
key_up = "Up"

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
Function to create a paddle, defined by player number and color.
"""
def paddle(pn, color):
    paddle = t.Turtle()
    paddle.speed(0)
    paddle.shape("square")
    paddle.color(color)
    paddle.shapesize(5, 1)
    paddle.up()
    paddle.goto(-(pn % 2 * 2 - 1) * sw/2.35, 0)
    paddle.velocity = 0
    return paddle

# Set up paddles
player = paddle(1, "deep sky blue")
opponent = paddle(2, "salmon")

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

# Set up ball
ball = t.Turtle()
ball.shape("square")
ball.color("white")
ball.shapesize(0.7)
ball.up()
ball.goto(0, 0)

while True: #needs to change to something != exit
    window.update()
    
    # Move up/down
    player.sety(clamp(player.ycor() + player.velocity*sh/180, (-sh/2)*0.7, (sh/2)*0.7))