import turtle

# Create a turtle object
t = turtle.Turtle()

# Set the fill color to blue
t.fillcolor("green")

# Begin filling a shape
t.begin_fill()

# Draw a square
for i in range(4):
    t.forward(500)
    t.left(90)

# End the fill
t.end_fill()

# Exit the turtle window
turtle.done()

