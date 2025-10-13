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
  
for i in range(6):    
    move() #i==6 will reach vict cond.
    jump()
    turn_left()
    
