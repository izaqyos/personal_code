from blackjack.src.player import player
from blackjack.src.card import card

def test_create_player():
    dealer = player("dealer")
    assert(dealer.name == "dealer")
    dealer.add_card(card(10))
    dealer.add_card(card(1))
    print(dealer)
    values = set()
    for v in dealer.cards.values():
        values.add(v.value)
    assert(values == {10,1})
    dealer.remove_card_by_value(1)
    assert({ v.value for v in dealer.cards.values()} == {10})
    dealer.remove_card(card(10))
    assert({ v.value for v in dealer.cards.values()} == set())

def test_add_cards():
    yosi = player("yosi")
    yosi.add_cards([card(i) for i in range(14,27)])
    print(yosi)

def test_score_calc_20():
    yosi = player("yosi")
    yosi.add_cards([card(10), card(11)])
    score = yosi.score
    #print(f"Yosi score is {score}")
    assert(score == 20)

def test_score_calc_higher_21_face():
    yosi = player("yosi")
    yosi.add_cards([card(13), card(11), card(5)])
    score = yosi.score
    #print(f"Yosi score is {score}")
    assert(score == 25)







def test_score_calc_ace():
    yosi = player("yosi")
    yosi.add_cards([card(13), card(1), card(5) ])
    score = yosi.score
    #print(f"Yosi score is {score}")
    assert(score == 16)


def test_score_calc_four_aces():
    yosi = player("yosi")
    yosi.add_cards([card(14), card(40), card(1), card(27), card(12) ])
    score = yosi.score
    #print(f"Yosi score is {score}")
    assert(score == 14)












def test_score_calc_lower_21():
    yosi = player("yosi")
    yosi.add_cards([card(9), card(6), card(1), card(3)])
    score = yosi.score
    #print(f"Yosi score is {score}")
    assert(score == 19)






