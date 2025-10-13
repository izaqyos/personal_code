import turtle

# Create a turtle object
t = turtle.Turtle()

# Draw a circle with rainbow colors
colors = ["red", "orange", "yellow", "green", "blue", "purple", "black", "brown", "pink",  "gray", ]
n = len(colors)
for i in range(n):
    t.pencolor(colors[i % n])
    t.fillcolor(colors[i % n])
    t.begin_fill()
    t.circle(200)
    t.end_fill()
    t.right(360//n)

# Exit the turtle window
turtle.done()

