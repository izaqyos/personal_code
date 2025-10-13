from blackjack.src.deck import deck
from blackjack.src.card import card


def test_create_deck():
    adeck = deck()
    print(adeck)

def test_remove_cards():
    adeck = deck()
    adeck._remove_card_from_deck(card(1))
    adeck._remove_card_from_deck(card(20))
    adeck._remove_card_from_deck(card(27))
    adeck._remove_card_from_deck(card(50))
    adeck._remove_card_from_deck(card(11))
    adeck._remove_card_from_deck_by_value(30)
    adeck._remove_card_from_deck_by_value(28)
    adeck._remove_card_from_deck_by_value(51)
    adeck._remove_card_from_deck_by_value(52)
    assert(adeck.size() == 43)
    #print(adeck)
    adeck._add_card_to_deck(card(1))
    adeck._add_card_to_deck_by_value(51)
    assert(adeck.size() == 45)

def test_remove_all_cards():
    adeck = deck()
    for i in range(1,53):
        adeck._remove_card_from_deck_by_value(i)
    assert(adeck.size() == 0)

def print_hand(hand):
    print("Hand is:")
    for card in hand:
        print(card, end="")

def test_deal_cards():
    adeck = deck()
    hand = adeck.deal_cards(2)
    print_hand(hand)
    assert(len(hand) == 2)
    assert(adeck.size() == 50)
    

