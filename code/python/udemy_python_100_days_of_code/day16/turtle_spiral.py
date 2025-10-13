import turtle

# Create a turtle object
t = turtle.Turtle()

from turtle import color, begin_fill, end_fill
color('blue', 'green')
begin_fill()

# Draw a spiral
for i in range(50):
    t.forward(i * 10)
    t.right(144)

# Exit the turtle window
end_fill()
turtle.done()

