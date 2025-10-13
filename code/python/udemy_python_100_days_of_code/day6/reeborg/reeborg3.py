http://reeborg.ca/reeborg.html?lang=en&mode=python&menu=worlds%2Fmenus%2Freeborg_intro_en.json&name=Hurdle%204&url=worlds%2Ftutorial_en%2Fhurdle4.json
'''
conditions
at_goal() front_is_clear() right_is_clear() wall_in_front()
wall_on_right() object_here() carries_object() is_facing_north()
'''
def turn_right():
    turn_left()
    turn_left()
    turn_left()
    
def jump():
    turn_left()
    steps = 0
    while wall_on_right():
        steps+=1
        move()
    turn_right()
    move()
    turn_right()
    while steps:
        steps-=1
        move()
    turn_left()
  
while not at_goal():
    if front_is_clear():
        move()
    else:
        if wall_in_front():
            jump()
