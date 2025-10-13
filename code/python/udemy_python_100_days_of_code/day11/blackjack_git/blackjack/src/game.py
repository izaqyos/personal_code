import src.card as card
import src.deck as deck
import src.player as player
from src.art import logo, win, win2, lose
from logger import mylogger

class InvalidNumberOfPlayers(Exception):
    """ Number of players is not valid """
    pass 

class game:
    '''
    blackjack game
    '''
    def __init__(self):
        mylogger.debug(f"{game.__init__.__qualname__}")
        self.players = [player.player("dealer")] 
        self.deck = deck.deck()
        self.human_player_name = "Player"
        self.max_num_players = 2

    def _game_setup(self):
        mylogger.debug(f"{game._game_setup.__qualname__}")
        #players = int(input(f"How many players? please choose 1-{self.max_num_players-1}... "))
        #if players<1 or players>self.max_num_players:
        #    print(f"can only choose 1-{self.max_num_players-1} players")
        #    raise InvalidNumberOfPlayers
        #else:
        #    for i in range(players):
        #        name = input("Please provide player name. name dealer is reserved. ")
        #        while name == "dealer":
        #            name = input("Please provide player name. name dealer is reserved. ")
        #        self.players.append(player.player(name))
        players = 1 #For now, only support one human player
        self.players.append(player.player(self.human_player_name))

    def __str__(self) -> str:
        ret = "Game state:\n"
        for player in self.players:
            ret+= f"{player}\n"
        return ret

    def _deal_to_all_players(self):
        mylogger.debug(f"{game._deal_to_all_players.__qualname__}")
        for player in self.players:
            self._deal_to_player(player)

    def _deal_to_player(self, player, num_cards=2):
        '''
        deal two cards to the player
        '''
        mylogger.debug(f"{game._deal_to_player.__qualname__}")
        player.add_cards(self.deck.deal_cards(num_cards))

    def _show_hands(self):
        mylogger.debug(f"{game._show_hands.__qualname__}")
        #Todo, print score for each player. calc Ace as 11 unless it's causing score to exceed 21 (in which case it is 1)
        for player in self.players:
            if player.name == "dealer":
                print(f"{player.name} top card is:")
                player_cards = list(player.cards.keys())
                print(player.cards[player_cards[-1]])
            else:
                print(f"player {player.name} hand is:")
                #ToDo, print hand more consicely. for 2 players it's ok. for more it's too much screen space
                for card in player.cards.values():
                    print(card)

    def _show_hand(self, player):
        for card in player.cards.values():
            print(card)
        

    def _is_winner(self):
        mylogger.debug(f"{game._is_winner.__qualname__}, player wants to end game {self._conclude_game}")
        lost = []
        winner = None
        victory = False #tie
        for player in self.players:
            if player.score == 21:
                mylogger.debug(f"{game._is_winner.__qualname__} player {player.name} has winning score of {player.score}")
                victory = True
                winner = player.name
                return victory, winner
            elif player.score > 21:
                mylogger.debug(f"{game._is_winner.__qualname__} player {player.name} has losing score of {player.score}")
                lost.append(player.name) 
        names = [player.name for player in self.players]
        non_losers = set(names) - set(lost)
        if len(non_losers) == 1:
            victory = True
            winner = list(non_losers)[0]
            mylogger.debug(f"{game._is_winner.__qualname__} player {player.name} is the only non losing. {len(non_losers)} have lost.")
            return victory, winner
        if self._conclude_game: # sort by higest score
            mylogger.debug(f"{game._is_winner.__qualname__} Player doesnt want to draw. Ending game and deciding highest score")
            players_scores = sorted( [(p.score, p.name) for p in self.players])
            if players_scores[-2] == players_scores [-1]:
                return False, None
            else:
                return True, players_scores[-1][1]
        return victory, winner
            

    def _should_cont_game(self):
        '''
        Assess victory or lose conditions. return False if met.
        '''
        mylogger.debug(f"{game._should_cont_game.__qualname__}")
        victory, winner = self._is_winner()
        return not (self._conclude_game or victory)


    def _check_players_status(self):
        mylogger.debug(f"{game._check_players_status.__qualname__}")
        import heapq
        scores = []
        winners = []
        for player in self.players:
            score = player.score
            if score > 21:
                mylogger.debug(f"player {player.name} went over and lost")
            elif score == 21:
                winners.append[player.name] 
            else:
                heapq.heappush(scores,(-score, player.name))
        mylogger.debug(f"scores {scores}  ")
        if winners:
            for player in winners:
                print(f"Player {player} has won!!")
        else:
            winner = scores[0][1]
            print(f"Player {winner} has won!!")
        


    def _should_dealer_draw(self):
        '''
        the "AI" of dealer. will use proabablity as our friend 
        '''
        mylogger.debug(f"{game._should_dealer_draw.__qualname__}")
        dealer = self.players[0]
        score = dealer.score
        ret = False
        if score > 21:
            mylogger.debug(f"{game._should_dealer_draw.__qualname__} dealer is overboard")
        elif score == 21:
            mylogger.debug(" dealer has won")
            ret = True
        elif score > 16:
            if dealer.has_ace():
                mylogger.debug(f"{game._should_dealer_draw.__qualname__} dealer has an ace and score {score}")
                ret = True #since ace can flip value to 1 
            else:
                mylogger.debug(f"{game._should_dealer_draw.__qualname__} dealer doesn't have an ace and score {score}")
                return False
        else:
            mylogger.debug(f"{game._should_dealer_draw.__qualname__} dealer score {score}")
            ret = True
        mylogger.debug(f"{game._should_dealer_draw.__qualname__} dealer shold draw {ret}")
        return ret

    def start_game(self):
        '''
        deal starting hand to each player
        show all players hands and scores
        show dealer top card only
        '''
        mylogger.debug(f"{game.start_game.__qualname__}")
        self._conclude_game = False
        self._game_setup()
        self._deal_to_all_players()
        self._show_hands()

        while self._should_cont_game():
            for player in self.players[1:]: #all but dealer
                ans=""
                while ans!='y' and ans!='n':
                    ans = input("Type 'y' to draw a card. 'n' to pass ") 
                if ans == 'y':
                    self._deal_to_player(player, 1) 
                    print("Your hand is:")
                    self._show_hand(self.players[1])
                else:
                    self._conclude_game = True
                if self._should_dealer_draw():
                    self._deal_to_player(self.players[0], 1) 
        victory, winner = self._is_winner()
        mylogger.debug(f"is winner check returned victory: {victory}, winner: {winner}")
        if victory:
            print("Dealer final hand is:")
            self._show_hand(self.players[0])
            print(f"{self.human_player_name} final hand is:")
            self._show_hand(self.players[1])
            if winner == self.human_player_name:
                print(win)
                print(f"{winner} winns!")
            else:
                print(lose)
                print(f"{self.human_player_name} - you lost! :(")
        else:
            print("Game ends in a tie")
        return

        
        



    def start(self):
        self.start_game()

