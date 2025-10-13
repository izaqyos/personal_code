'''
The conditions front_is_clear() or wall_in_front(), at_goal(), and their negation.
'''
def turn_right():
    turn_left()
    turn_left()
    turn_left()
    
def jump():
    turn_left()
    move()
    turn_right()
    move()
    turn_right()
    move()
    turn_left()
  
while not at_goal():
    if front_is_clear():
        move()
    else:
        if wall_in_front():
            jump()

         
    
