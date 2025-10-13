# Step 1: Make all the "turtle" commands available to us.
import turtle

# Step 2: Create a new turtle. We'll call it "bob"
bob = turtle.Turtle()

# Step 3: Move in the direction Bob's facing for 50 pixels
bob.forward(350)

# Step 4: We're done!
turtle.done()

def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)

