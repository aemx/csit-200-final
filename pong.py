import turtle as t
from time import sleep
from random import uniform as random

# Global variables
sw, sh = 1280, 720
speed_x, speed_y = 6*sw/1280, 6*sh/720
key_down = "Down"
key_up = "Up"

"""
Code for the Text class, a Turtle object that has the ability to display strings.
"""
class Text:
    def __init__(self, string="", color="FFFFFF", size=12, xpos=0, ypos=0):
        """
        A constructor that loads a Turtle object, then initalizes five attributes.
        """
        self.turtle = t.Turtle()
        self.turtle.up()
        self.__string = str(string)
        self.__color = color
        self.__size = size
        self.__xpos = xpos
        self.__ypos = ypos

    def __load(self):
        """
        A private function that loads data entered from the object.
        """
        self.turtle.color(self.__color)
        self.turtle.goto(self.__xpos, self.__ypos)
        self.turtle.write(str(self.__string), True, "right", ("Pong Score", self.__size))
        self.turtle.hideturtle()
        self.turtle.up()

    def update(self, newstring):
        """
        A function that updates the Text object with a new string.
        """
        self.__string = str(newstring)
        self.turtle.clear()
        self.__load()

def clamp(num, lo, hi):
    """
    Clamps a value at a minimum and maximum.
    """
    return min(max(lo, num), hi)

def make_shape(color, length, width, xpos, ypos):
    """
    Generates a square or rectangle on the screen.
    """
    shape = t.Turtle()
    shape.shape("square")
    shape.color(color)
    shape.shapesize(length, width)
    shape.up()
    shape.goto(xpos, ypos)
    return shape

def make_paddle(pn, color):
    """
    Generates a paddle, defined by player number and color.
    """
    paddle = make_shape(color, 5, 1, -(pn % 2 * 2 - 1) * sw/2.35, 0)
    paddle.velocity = 0
    paddle.score = 0
    return paddle

def new_window():
    """
    Brings up a window and sets some settings in Turtle.
    """ 
    # Turn off drawing animations
    t.tracer(0, 0)

    # Initialize the game's window
    window = t.Screen()
    window.title("PyPong")
    window.setup(sw, sh)
    window.bgcolor("black")
    
    # Return the window
    return window

def start_round(window, player, opponent, ball, score_p1, score_p2):
    """
    A function to start a new round of Pong.
    """ 
    # Remove the ball from the screen
    ball.goto(0, sh*2)
    
    # Set scores
    score_p1.update(player.score)
    score_p2.update(opponent.score)
    window.update()
    sleep(1)
    
    # Reset the positions of each paddle
    player.sety(0)
    opponent.sety(0)
    
    # Set the opponent's accuracy
    opponent.hitpos = random(0, 70)
    
    # Serve the ball at a random angle and y position
    ball.velocity_x, ball.velocity_y = -1*random(0.8, 1.3), random(0.8, 1.3)
    ball.goto(0, random(-(sh/2)+16, (sh/2)-16))
    window.update()

def main():
    """
    The main function, which starts a new game of Pong.
    """
    
    # Make a new window
    window = new_window()

    # Set up paddles
    player = make_paddle(1, "#4b8bbe")
    opponent = make_paddle(2, "#ffe873")

    # Player control
    # player_stop_up/down prevents stutter when both keys are pressed.
    def player_up(): player.velocity = 1
    def player_down(): player.velocity = -1
    def player_stop_up():
        if player.velocity == 1: player.velocity = 0
    def player_stop_down():
        if player.velocity == -1: player.velocity = 0

    # Keyboard bindings
    window.onkeypress(player_up, key_up)
    window.onkeypress(player_down, key_down)
    window.onkeyrelease(player_stop_up, key_up)
    window.onkeyrelease(player_stop_down, key_down)
    window.listen()

    # Set up divider
    for i in range(int(-sh/1.5), int(sh/1.5), 60):
        make_shape("grey", 2, 0.7, 0, i)

    # Set up ball
    ball = make_shape("white", 0.7, 0.7, 0, 0)

    # Set up scoreboard
    score_p1 = Text(player.score, "#4b8bbe", 120, -sw/2.8+sw/3.8, sh/4)
    score_p2 = Text(opponent.score, "#ffe873", 120, sw/2.8, sh/4)

    # Start a new round by default
    start_round(window, player, opponent, ball, score_p1, score_p2)

    # Update loop
    while True:

        # Player movement
        player.sety(clamp(player.ycor() + player.velocity*speed_y, (-sh/2)+60, (sh/2)-60))

        # Opponent movement
        opponent.sety(clamp(ball.ycor() + opponent.hitpos, (-sh/2)+60, (sh/2)-60))

        # Ball collision/movement
        ball.velocity_y *= -1 if abs(ball.ycor()) >= (sh/2)-16 else 1
        ball.goto(ball.xcor() + ball.velocity_x*speed_x, ball.ycor() + ball.velocity_y*speed_y)

        # Paddle collision for player
        # Also, generate a new position for the opponent to follow
        if -sw/2.35+5 <= ball.xcor() <= -sw/2.35+20 and \
        player.ycor()-62 <= ball.ycor() <= player.ycor()+62:
            ball.velocity_x *= -1
            opponent.hitpos = random(0, 75)

        # Paddle collision logic for opponent
        ball.velocity_x *= -1 if sw/2.35-20 <= ball.xcor() <= sw/2.35-5 and \
        opponent.ycor()-62 <= ball.ycor() <= opponent.ycor()+62 else 1

        # Update the window @ 144 Hz
        window.update()
        sleep(1/144)
        
        # But, if the ball goes out of bounds...add to the score, and start a new round
        if abs(ball.xcor()) >= (sw/2.1):
            
            # Add to the score
            if ball.xcor() > 0:
                player.score += 1
            else:
                opponent.score += 1
                
            # Start a new round if no player has 15 points
            if player.score == 15:
                quit()
            elif opponent.score == 15:
                quit()
            else:
                start_round(window, player, opponent, ball, score_p1, score_p2)

if __name__ == "__main__":
    main()