import turtle

# Create a turtle screen
screen = turtle.Screen()

# Create a turtle
my_turtle = turtle.Turtle()

# Write text using the turtle
my_turtle.write("Hello, Turtle!", align="center", font=("Arial", 16, "bold"))

# Hide the turtle
my_turtle.hideturtle()

# Keep the window open
turtle.done()
