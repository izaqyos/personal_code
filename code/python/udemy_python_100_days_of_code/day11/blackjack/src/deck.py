import src.card as card
import random
from logger import mylogger

class InvalidValueExpection(Exception):
    """ Value is not valid """
    pass 

class NotEnoughCardsExpection(Exception):
    """ There are not enough cards in the deck """
    pass 

class deck:
    """
    A deck of cards
    """

    def __init__(self):
        self.cards = {k:card.card(k) for k in range(1,53)}
        # self.dealt = set() # not needed, just calculate by set diff operator

    def __str__(self):
        ret = ""
        for k,v in self.cards.items():
            ret+=str(v)
            if k%card.card.card_family_size == 0:
                ret+="\n"
        return ret

    def size(self):
        return len(self.cards)

    def get_dealt_cards(self): 
        mylogger.debug(f"{deck.get_dealt_cards.__qualname__}")
        allcards = {_ for _ in range(1, 53)} 
        deck_cards = set(self.cards.keys()) 
        return allcards-deck_cards
 

    def _remove_card_from_deck(self, card):
        mylogger.debug(f"{deck._remove_card_from_deck.__qualname__}")
        ret =self.cards[card.value] 
        del self.cards[card.value]
        return ret

    def _add_card_to_deck(self, card):
        mylogger.debug(f"{deck._add_card_to_deck.__qualname__}")
        self.cards[card.value] = card


    def _remove_card_from_deck_by_value(self, value):
        mylogger.debug(f"{deck._remove_card_from_deck_by_value.__qualname__}")
        mylogger.debug(f"[debug] dealing card {value}")
        ret = None
        if value in self.cards:
            ret =self.cards[value] 
            del self.cards[value]
        else:
            mylogger.warning(f"[warn] card {value} is not in deck cards!")
        return ret

    def _add_card_to_deck_by_value(self, value):
        mylogger.debug(f"{deck._add_card_to_deck_by_value.__qualname__}")
        self.cards[value] = card.card(value)

    def deal_cards(self, num_cards):
        mylogger.debug(f"{deck.deal_cards.__qualname__}")
        if num_cards<0 or num_cards>53:
            raise InvalidValueExpection
        if num_cards > len(self.cards):
            raise NotEnoughCardsExpection

        ret_cards = []
        for i in range(num_cards):
            ret_cards.append(self._remove_card_from_deck_by_value(random.choice(list(self.cards.keys())) ))

            #while True:
            #    val = random.randint(1,52)
            #    if val in self.cards:
            #        ret_cards.append(self._remove_card_from_deck_by_value(val))
            #        break
        return ret_cards

            



