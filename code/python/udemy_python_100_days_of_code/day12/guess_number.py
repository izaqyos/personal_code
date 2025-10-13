logo = '''

                                                      .-.                                                                  
  .--.    ___  ___    .--.       .--.        .--.    ( __)  ___ .-.     .--.       .--.     .---.   ___ .-. .-.     .--.   
 /    \  (   )(   )  /    \    /  _  \     /  _  \   (''") (   )   \   /    \     /    \   / .-, \ (   )   '   \   /    \  
;  ,-. '  | |  | |  |  .-. ;  . .' `. ;   . .' `. ;   | |   |  .-. .  ;  ,-. '   ;  ,-. ' (__) ; |  |  .-.  .-. ; |  .-. ; 
| |  | |  | |  | |  |  | | |  | '   | |   | '   | |   | |   | |  | |  | |  | |   | |  | |   .'`  |  | |  | |  | | |  | | | 
| |  | |  | |  | |  |  |/  |  _\_`.(___)  _\_`.(___)  | |   | |  | |  | |  | |   | |  | |  / .'| |  | |  | |  | | |  |/  | 
| |  | |  | |  | |  |  ' _.' (   ). '.   (   ). '.    | |   | |  | |  | |  | |   | |  | | | /  | |  | |  | |  | | |  ' _.' 
| '  | |  | |  ; '  |  .'.-.  | |  `\ |   | |  `\ |   | |   | |  | |  | '  | |   | '  | | ; |  ; |  | |  | |  | | |  .'.-. 
'  `-' |  ' `-'  /  '  `-' /  ; '._,' '   ; '._,' '   | |   | |  | |  '  `-' |   '  `-' | ' `-'  |  | |  | |  | | '  `-' / 
 `.__. |   '.__.'    `.__.'    '.___.'     '.___.'   (___) (___)(___)  `.__. |    `.__. | `.__.'_. (___)(___)(___) `.__.'  
 ( `-' ;                                                               ( `-' ;    ( `-' ;                                  
  `.__.                                                                 `.__.      `.__.                                   

'''

import random 
class GuessingGame():
    def __init__(self):
        self.log = logo
        self.range_low =1
        self.range_high =100

    def run_game(self):
        number = random.randint(self.range_low,self.range_high)
        intro_msg = "Welcome to the Number Guessing Game!\n"
        intro_msg += f"Range is between {self.range_low} and {self.range_high}"
        print(logo)
        print(intro_msg)
        print(f"[debug] number is {number}")
        difficulty = ''
        attempts = {'easy': 5, 'hard': 10}

        while not(difficulty=='easy' or difficulty=='hard'):
            difficulty = input("Choose difficulty. Type 'easy' or 'hard': ")
        max_attempts = attempts[difficulty]
        for i in range(max_attempts):
            print(f"You have {max_attempts-i} guesses left")
            guess = int(input("Make your guess: "))
            if guess > number:
                print("Too high.")
            elif guess<number:
                print("Too low.")
            else:
                print(f"Awesome! You got it. The number was {number}")
                return
        print("No more guesses. you lose :(")


def main():
    game = GuessingGame()
    game.run_game()

if __name__ == "__main__":
    main()
