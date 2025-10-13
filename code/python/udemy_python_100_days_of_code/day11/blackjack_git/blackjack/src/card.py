from enum import Enum
import src.art as art
#import art 

#class CARDTYPE(Enum):
#    CLUBS = 0
#    DIAMONDS = 1
#    HEARTS = 2
#    SPADES =3

class InvalidValueExpection(Exception):
    """ Value is not valid """
    pass 

class card:

    """
   A card abstraction 
    """
    card_family_size = 13
    card_families = 4
    deck_size = card_family_size*card_families
    card_types={
            0: "clubs",
            1: "diamonds",
            2: "hearts",
            3: "spades",
            }
    card_names={
            0 : "ace",
            1 : "two",
            2 : "three",
            3 : "four",
            4 : "five",
            5 : "six",
            6 : "seven",
            7 : "eight",
            8 : "nine",
            9 : "ten",
            10: "jack",
            11: "queen",
            12: "king",
            }

    def __init__(self, value):
        """ create a card """
        if value <1 or value >52:
            raise InvalidValueExpection(f"Value {value} is not valid for a card")
        self._value = value
        #print(f"initializing card {value}")
        self.type = self.card_types[self._normalize_value_type(value)] 
        if (value-1)//self.card_family_size == 0:
            self.art = art.clubs[self._normalize_value(value)]
        elif (value-1)//self.card_family_size == 1:
            self.art = art.diamonds[self._normalize_value(value)]
        elif (value-1)//self.card_family_size == 2:
            self.art = art.hearts[self._normalize_value(value)]
        elif (value-1)//self.card_family_size == 3:
            self.art = art.spades[self._normalize_value(value)]

    def _normalize_value_type(self, value):
        return (value-1)//self.card_family_size

    def _normalize_value(self, value):
        return (value-1)%self.card_family_size

    def print(self):
        print(f"{self.card_names[self._normalize_value(self._value)]} of {self.type}. {self.art}")

    def __str__(self):
        return f"{self.card_names[self._normalize_value(self._value)]} of {self.type}. {self.art}"

    @property 
    def value(self):
        return self._value

    #@property.setter
    #def value(newval):
    #    if value <1 or value >52:
    #        print(f"valid values are in range 1-52. {newval} is not valid")
    #    else:
    #        self._value = newval


        
