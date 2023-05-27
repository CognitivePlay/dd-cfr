from dd_cfr.games.schnapsen.card import Card
from dd_cfr.games.schnapsen.card_value import CardValue
from dd_cfr.games.schnapsen.suit import Suit


def test_values():
    for suit in list(Suit):
        for value in list(CardValue):
            card = Card(suit, value)

            assert card.suit == suit
            assert card.card_value == value


def test___eq__():
    ace_of_spades = Card(Suit.SPADES, CardValue.ACE)
    assert ace_of_spades == ace_of_spades

    assert ace_of_spades == Card(Suit.SPADES, CardValue.ACE)

    assert not ace_of_spades == (Suit.SPADES, CardValue.ACE)
    assert ace_of_spades != (Suit.SPADES, CardValue.ACE)

    assert not ace_of_spades == Card(Suit.SPADES, CardValue.KING)
    assert ace_of_spades != Card(Suit.SPADES, CardValue.KING)

    assert not ace_of_spades == (Suit.HEARTS, CardValue.ACE)
    assert ace_of_spades != (Suit.HEARTS, CardValue.ACE)
