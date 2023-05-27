from dd_cfr.games.schnapsen.card import Card
from dd_cfr.games.schnapsen.card_value import CardValue
from dd_cfr.games.schnapsen.suit import Suit


def test_getters():
    for suit in list(Suit):
        for value in list(CardValue):
            card = Card(suit, value)

            assert card.get_suit() == suit
            assert card.get_card_value() == value
