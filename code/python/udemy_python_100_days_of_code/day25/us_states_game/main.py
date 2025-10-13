#!/opt/homebrew/bin/python3
import turtle
import pandas


##This code adds a callback to mouse clicks so I can manually find the coordinates of each state on the image by clicking it
#def get_mouse_click_coordinates(x,y):
#    print(x,y)
#turtle.onscreenclick(get_mouse_click_coordinates) #add callback to onscreenclick 
#turtle.mainloop()
##screen.exitonclick()

def load_states():
    states_fname = "50_states.csv"
    states_dframe = pandas.read_csv(states_fname)
    ##ToDo, use this example to get coordinates of state and write it's name using turtle at these coordinates
    #delaware_row = states_dframe[states_dframe.state == 'Delaware']
    #print(f"delaware coordinates: { states_dframe.iloc[delaware_row.index]['x'].tolist()[0] ,states_dframe.iloc[delaware_row.index]['y'].tolist()[0]  }")
    return states_dframe

def load_coordinates(states_dframe):
    #state_coordinates = dict()
    state_coordinates = { t[0].lower():(t[1],t[2]) for t in zip(states_dframe["state"], states_dframe["x"], states_dframe["y"])} 
    #print(f"Built states to coordinates dictionary {state_coordinates}")
    return state_coordinates

def write_name(name, x, y):
    new_turtle = turtle.Turtle()
    new_turtle.pu()
    new_turtle.goto(x,y)
    new_turtle.write(name, move=False, align="center", font=("Arial", 20, "normal"))

def load_screen():
    title = "US states game"
    screen = turtle.Screen()
    screen.title(title)
    image_file = "blank_states_img.gif"
    screen.addshape(image_file)
    turtle.shape(image_file)
    return screen

def main():
    screen = load_screen()
    states_df  = load_states()
    state_coordinates = load_coordinates(states_df)

    states = states_df["state"].unique().tolist() 
    states = [ _.lower() for _ in states]
    guessed = []
    print(f"Loaded US states: {states}")
    num_states, num_guessed = len(states), 0
    while num_guessed < num_states: 
        answer_state = screen.textinput(title=f"{num_guessed}/{num_states} states guessed correctly", prompt="What's another states name?").lower()
        #print(f"You anwered {answer_state}")
        if answer_state == "exit":
            break
        if answer_state in states:
            num_guessed += 1 
            #print(f"You answered correctly. in total you guessed {num_guessed}/{num_states}")
            guessed.append(answer_state)
            states.remove(answer_state)
            #print(f"printing answer: {answer_state, state_coordinates[answer_state][0], state_coordinates[answer_state][1]}")

            write_name(answer_state, state_coordinates[answer_state][0], state_coordinates[answer_state][1])
            #alternative way. get state row and use it to get x,y. as in:
            #state_row = states_df[states_df.state == answer_state]
            #write_name(answer_state, (state_row.x), int(state_row.y)) 
            #we can also get the state scalar from the row like
            #write_name(state_row.state.item(), (state_row.x), int(state_row.y)) 

            #remove row of guessed state
            states_df = states_df[states_df.state != answer_state.title() ]


    states_df.to_csv("unguessed_states.csv", index=False)
    ##exit with click
    #screen.exitonclick()

if __name__ == "__main__":
    main()

