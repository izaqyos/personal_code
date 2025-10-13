from blackjack.src.card import card
from blackjack.src.card import InvalidValueExpection

def test_invalid_card():
    try:
        acard = card(0)
    except InvalidValueExpection:
        assert True 
    try:
        acard = card(54)
    except InvalidValueExpection:
        assert True 
    try:
        acard = card(7)
    except InvalidValueExpection:
        assert False 

def test_face_card():
    acard = card(11)
    print(acard)

def test_gen_full_deck():
    for i in range(1,53):
        acard = card(i)
        print(acard, end=" ")

def test_get_value():
    acard = card(11)
    value = acard.value
    assert(value == 11)

