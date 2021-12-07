import turtle as t

# Set up resolution-dependant variables
sw, sh = 1280, 720

# Initialize the game's window
window = t.Screen()
window.title("Pong")
window.setup(width=sw, height=sh)
window.bgcolor("black")

"""
Function to create a paddle, defined by player number and color.
"""
def paddle(pn, color):
    paddle = t.Turtle()
    paddle.speed(0)
    paddle.shape("square")
    paddle.color(color)
    paddle.shapesize(5, 1)
    paddle.penup()
    paddle.goto((pn % 2 * 2 - 1) * sw/2.5, 0)
    return paddle

# Set up paddles
player = paddle(1, "red")
opponent = paddle(2, "blue")

# Set up ball
ball = t.Turtle()
ball.shape("square")
ball.color("white")
ball.shapesize(0.7)
ball.penup()
ball.goto(0, 0)

while True: #needs to change to something != exit
    window.update()