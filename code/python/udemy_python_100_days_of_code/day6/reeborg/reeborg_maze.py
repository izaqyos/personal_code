'''
The conditions front_is_clear() or wall_in_front(), at_goal(), and their negation.

Lost in a maze
Reeborg was exploring a dark maze and the battery in its flashlight ran out.

Write a program using an if/elif/else statement so Reeborg can find the exit. 
The secret is to have Reeborg follow along the right edge of the maze,
turning right if it can, going straight ahead if it can’t turn right, or turning left as a last resort.

What you need to know
The functions move() and turn_left().
Either the test front_is_clear() or wall_in_front(), right_is_clear() or wall_on_right(), and at_goal().
How to use a while loop and if/elif/else statements.
It might be useful to know how to use the negation of a test (not in Python).
Difficulty level
'''

'''
Following code works for most cases.
It fails if Reeborg starts in an all open space.
Then it will always have the right clear so it will get stuck in an infinite loop
'''
#def turn_right():
#    turn_left()
#    turn_left()
#    turn_left()
#    
#    
#while not at_goal():
#    if right_is_clear():
#        turn_right()
#        move()
#    elif front_is_clear():
#        move()
#    else:
#        turn_left()

def turn_right():
    turn_left()
    turn_left()
    turn_left()
    

#identify state leading to infinite loop
def is_all_clear():
    for i in range(4):
        if not front_is_clear():
            return False
        turn_left()
    return True

#if we are at this state change to state: there's a wall to our right
if is_all_clear():
    #first move untill Reeborg hits a wall
    while not at_goal() and front_is_clear(): 
        move()
    # now pivot so we have a wall to right
    while not wall_on_right():
        turn_left()
    
'''
My code above can be simplified. just run until you hit a wall. then turn left (so wall is to your right)
while front_is_clear():
    move()
turn_left()
'''
#now we are at the state that guarantees  successful exit (that's how the mazes are designed)
while not at_goal():
    if right_is_clear():
        turn_right()
        move()
    elif front_is_clear():
        move()
    else:
        turn_left()
