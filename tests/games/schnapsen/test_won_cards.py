import pytest

from dd_cfr.games.schnapsen.card import Card
from dd_cfr.games.schnapsen.card_value import CardValue
from dd_cfr.games.schnapsen.suit import Suit
from dd_cfr.games.schnapsen.won_cards import WonCards


def test_get_number_of_cards():
    won_cards = WonCards()

    assert won_cards.get_number_of_cards() == 0

    won_cards.add_card(Card(Suit.HEARTS, CardValue.TEN))
    assert won_cards.get_number_of_cards() == 1

    won_cards.add_card(Card(Suit.HEARTS, CardValue.JACK))
    assert won_cards.get_number_of_cards() == 2


def test_add_card():
    won_cards = WonCards()

    won_cards.add_card(Card(Suit.HEARTS, CardValue.TEN))
    won_cards.add_card(Card(Suit.HEARTS, CardValue.JACK))

    with pytest.raises(ValueError):
        won_cards.add_card(Card(Suit.HEARTS, CardValue.JACK))

    won_cards.add_card(Card(Suit.DIAMONDS, CardValue.JACK))


def test_get_number_of_points():
    won_cards = WonCards()

    assert won_cards.get_number_of_points() == 0

    won_cards.add_card(Card(Suit.HEARTS, CardValue.TEN))
    assert won_cards.get_number_of_points() == CardValue.TEN.get_points()

    won_cards.add_card(Card(Suit.HEARTS, CardValue.JACK))
    assert (
        won_cards.get_number_of_points()
        == CardValue.TEN.get_points() + CardValue.JACK.get_points()
    )

    won_cards.add_card(Card(Suit.DIAMONDS, CardValue.JACK))
    assert (
        won_cards.get_number_of_points()
        == CardValue.TEN.get_points() + 2 * CardValue.JACK.get_points()
    )


def test___contains__():
    won_cards = WonCards()

    assert Card(Suit.HEARTS, CardValue.TEN) not in won_cards
    assert Card(Suit.HEARTS, CardValue.JACK) not in won_cards
    assert Card(Suit.DIAMONDS, CardValue.JACK) not in won_cards

    won_cards.add_card(Card(Suit.HEARTS, CardValue.TEN))
    assert Card(Suit.HEARTS, CardValue.TEN) in won_cards
    assert Card(Suit.HEARTS, CardValue.JACK) not in won_cards
    assert Card(Suit.DIAMONDS, CardValue.JACK) not in won_cards

    won_cards.add_card(Card(Suit.HEARTS, CardValue.JACK))
    assert Card(Suit.HEARTS, CardValue.TEN) in won_cards
    assert Card(Suit.HEARTS, CardValue.JACK) in won_cards
    assert Card(Suit.DIAMONDS, CardValue.JACK) not in won_cards

    won_cards.add_card(Card(Suit.DIAMONDS, CardValue.JACK))
    assert Card(Suit.HEARTS, CardValue.TEN) in won_cards
    assert Card(Suit.HEARTS, CardValue.JACK) in won_cards
    assert Card(Suit.DIAMONDS, CardValue.JACK) in won_cards
