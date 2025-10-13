import sys, os
#sys.path.append('/Users/i500695/work/code/python/udemy_python_100_days_of_code/day11/blackjack')

sys.path.append(os.getcwd())
from game import game
from logger import mylogger
from src.art import logo

def main():
    mylogger.debug(f"{main.__qualname__}")
    print(logo)
    while True:
        ans = input("Do you want to play a game of blackjack? Type 'y' or 'n': ")
        if ans == 'y':
            agame = game()
            agame.start()
        else:
            return

if __name__ == '__main__':
    main()
    