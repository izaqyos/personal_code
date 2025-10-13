from blackjack.src.game import game

def test_create_game():
    newgame = game()
    newgame.start()
    #print(newgame)