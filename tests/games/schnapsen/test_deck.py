import pytest
import random
import typing

from dd_cfr.games.schnapsen.card import Card
from dd_cfr.games.schnapsen.card_value import CardValue
from dd_cfr.games.schnapsen.deck import Deck
from dd_cfr.games.schnapsen.suit import Suit


def assert_all_cards_exist_once(list_of_cards: typing.List[Card]):
    all_cards = Deck._get_list_of_all_cards()
    assert len(all_cards) == len(list_of_cards)

    for card in all_cards:
        found = False
        for other_card in list_of_cards:
            if card == other_card:
                found = True
                break
        assert found, card


def test___init__():
    deck_default_rng_1 = Deck()
    deck_default_rng_2 = Deck()
    deck_seeded_rng_1 = Deck(random.Random(0))
    deck_seeded_rng_2 = Deck(random.Random(0))

    assert_all_cards_exist_once(deck_default_rng_1._cards)
    assert_all_cards_exist_once(deck_default_rng_2._cards)
    assert_all_cards_exist_once(deck_seeded_rng_1._cards)
    assert_all_cards_exist_once(deck_seeded_rng_2._cards)

    assert deck_default_rng_1._cards != deck_default_rng_2._cards
    assert deck_default_rng_1._cards != deck_seeded_rng_1._cards
    assert deck_default_rng_1._cards != deck_seeded_rng_2._cards

    assert deck_seeded_rng_1._cards == deck_seeded_rng_2._cards


def test_get_maximum_number_of_cards():
    assert Deck.get_maximum_number_of_cards() == len(Suit) * len(CardValue)


def test_get_number_of_cards():
    deck = Deck()
    expected = deck.get_maximum_number_of_cards()

    for _ in range(deck.get_maximum_number_of_cards()):
        assert deck.get_number_of_cards() == expected
        deck.deal_top_card()
        expected -= 1

    assert deck.get_number_of_cards() == 0


def test_get_turn_up_card():
    deck = Deck()
    expected = deck._cards[-1]

    assert deck.get_number_of_cards() == deck.get_maximum_number_of_cards()
    assert deck.get_turn_up_card() == expected

    # Turn-up card is not removed:
    assert deck.get_number_of_cards() == deck.get_maximum_number_of_cards()
    assert deck.get_turn_up_card() == expected

    # No change when other cards are dealt:
    for _ in range(deck.get_maximum_number_of_cards()):
        assert deck.get_turn_up_card() == expected
        deck.deal_top_card()

    # Raises if no cards are left:
    with pytest.raises(ValueError):
        deck.get_turn_up_card()


def test_deal_top_card():
    deck = Deck()

    for i in range(deck.get_maximum_number_of_cards()):
        expected = deck._cards[0]
        assert deck.get_number_of_cards() == deck.get_maximum_number_of_cards() - i
        assert deck.deal_top_card() == expected

    assert deck.get_number_of_cards() == 0

    with pytest.raises(ValueError):
        deck.deal_top_card()


def test__get_list_of_all_cards():
    expected = []
    for suit in list(Suit):
        for value in list(CardValue):
            expected.append(Card(suit, value))

    assert len(expected) == 4 * 5
    assert expected == Deck._get_list_of_all_cards()
