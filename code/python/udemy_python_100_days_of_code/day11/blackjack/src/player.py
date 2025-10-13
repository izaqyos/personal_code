import src.card as card
import src.deck as deck
from logger import mylogger

class InvalidPlayerName(Exception):
    """ Name of player is not valid """
    pass 


class player:
    '''
    a blackjack player
    '''
    #_name = ""
    #_cards = dict()

    def __init__(self, name):
        self._name = name
        self._cards = dict() # dict. k=card value, v=Reference to card

        #game class does input validation. player should remain unbound to game logic
        #if name == "dealer":
        #    print("Can't choose name dealer")
        #    raise InvalidPlayerName
        #else:
        #    self._name == name
        #    self._cards ==  {} # dict. k=card value, v=Reference to card
        #self._cards ==  {} # dict. k=card value, v=Reference to card

    def add_cards(self, cards):
        for card in cards:
            self.add_card(card)

    def add_card(self, card):
        mylogger.debug(f" adding card {card} to {self.name}")
        if not card:
            mylogger.error(f" Got an invalid card {card}")
        k = card._value 
        if k in self.cards:
            mylogger.warning(f" Player already has this card {card}")
        else:
            self.cards[k] = card

    def remove_card_by_value(self, value):
        k = value 
        if k in self.cards:
            del self.cards[k]

    def remove_card(self, card):
        k = card._value 
        if k in self.cards:
            del self.cards[k]

    @property 
    def name(self):
        return self._name

    @property 
    def cards(self):
        return self._cards

    def _calc_score(self):
        threshold = 21
        dealer_name =  "dealer"
        card_values = [k%13 for k in self.cards] #normalize values to range 0 (kings) to 12 (queen)
        card_values = list(map(lambda x: 10 if x>10 or x==0 else x, card_values)) # face cards get 10, kings%13 is 0...
        card_values = list(map(lambda x: 11 if x==1 else x, card_values)) #aces get value of 11 
        score = sum(card_values)
        mylogger.info(f"normalized card values {card_values}, score {score}, threshold {threshold}")
        if player.name != dealer_name:
            ace_values = {1,14, 27, 40}
            num_aces = len(ace_values.intersection(set(self.cards)) )
            mylogger.debug(f"num of aces is {num_aces}")
            while score > threshold and num_aces>0:
                score -=10
                num_aces -=1 #try to assign value of 1 to an ace. instead of 11
                mylogger.debug(f"updated score to {score}, num aces to {num_aces}")
        return score


    def has_ace(self):
        for ace in [1,14,27, 40]:
            if ace in self.cards:
                return True
        return False

    @property 
    def score(self):
        return self._calc_score()

    def __str__(self):
        ret = f"Player name is {self._name}\n"
        ret+= f"Hands is:\n"
        for card in self._cards.values():
            ret+=str(card)
        return ret










