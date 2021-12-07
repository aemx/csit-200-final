import turtle as t

# Set up resolution-dependant variables
sw, sh = 1280, 720

# Initialize the game's window
window = t.Screen()
window.title("Pong")
window.setup(width=sw, height=sh)
window.bgcolor("black")



while True: #needs to change to something != exit
    window.update()