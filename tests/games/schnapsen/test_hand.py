import pytest

from dd_cfr.games.schnapsen.deck import Deck
from dd_cfr.games.schnapsen.hand import Hand


def test___init__():
    for number_of_cards in range(10):
        deck = Deck()

        if number_of_cards == 5:
            Hand([deck.deal_top_card() for _ in range(number_of_cards)])
        else:
            with pytest.raises(ValueError):
                Hand([deck.deal_top_card() for _ in range(number_of_cards)])


def test_get_number_of_cards():
    deck = Deck()
    hand = Hand([deck.deal_top_card() for _ in range(5)])

    assert hand.get_number_of_cards() == 5


def test_get_card():
    deck = Deck()
    initial_cards = [deck.deal_top_card() for _ in range(5)]
    hand = Hand(initial_cards)

    for i in range(5):
        assert hand.get_card(i) == initial_cards[i]

    for i in [-1, 5, 6]:
        with pytest.raises(IndexError):
            hand.get_card(i)

    for _ in range(5):
        hand.play(0)
        for i in range(-1, 7):
            if i >= 0 and i < hand.get_number_of_cards():
                continue
            expected = IndexError if hand.get_number_of_cards() > 0 else ValueError
            with pytest.raises(expected):
                hand.get_card(i)


def test_play():
    deck = Deck()
    initial_cards = [deck.deal_top_card() for _ in range(5)]
    hand = Hand(initial_cards)

    assert hand.get_card(0) == initial_cards[0]
    assert hand.get_card(1) == initial_cards[1]
    assert hand.get_card(2) == initial_cards[2]
    assert hand.get_card(3) == initial_cards[3]
    assert hand.get_card(4) == initial_cards[4]

    # Play one card:
    assert hand.play(3) == initial_cards[3]

    assert hand.get_number_of_cards() == 4

    assert hand.get_card(0) == initial_cards[0]
    assert hand.get_card(1) == initial_cards[1]
    assert hand.get_card(2) == initial_cards[2]
    assert hand.get_card(3) == initial_cards[4]

    for i in [-1, 4, 5, 6]:
        with pytest.raises(IndexError):
            hand.play(i)

    # Play another two cards:
    assert hand.play(3) == initial_cards[4]
    assert hand.play(1) == initial_cards[1]

    assert hand.get_number_of_cards() == 2

    assert hand.get_card(0) == initial_cards[0]
    assert hand.get_card(1) == initial_cards[2]

    for i in [-1, 2, 3, 4, 5, 6]:
        with pytest.raises(IndexError):
            hand.play(i)

    # Play the remaining cards:
    assert hand.play(0) == initial_cards[0]
    assert hand.play(0) == initial_cards[2]

    assert hand.get_number_of_cards() == 0

    for i in [-1, 0, 1, 2, 3, 4, 5, 6]:
        with pytest.raises(ValueError):
            hand.play(i)


def test_draw():
    deck = Deck()
    initial_cards = [deck.deal_top_card() for _ in range(5)]
    hand = Hand(initial_cards)

    with pytest.raises(ValueError):
        hand.draw(deck)

    expected = initial_cards[:]

    hand.play(0)
    expected.pop(0)
    expected.append(deck._cards[0])
    hand.draw(deck)

    for i in range(5):
        assert hand.get_card(i) == expected[i]

    hand.play(3)
    expected.pop(3)
    expected.append(deck._cards[0])
    hand.draw(deck)

    for i in range(5):
        assert hand.get_card(i) == expected[i]

    for _ in range(deck.get_number_of_cards()):
        deck.deal_top_card()

    hand.play(0)

    with pytest.raises(ValueError):
        hand.draw(deck)

    # Cannot draw with hand with 3 or fewer cards:
    deck = Deck()
    hand = Hand(initial_cards)

    hand.play(0)
    hand.draw(deck)

    hand.play(0)
    for _ in range(4):
        hand.play(0)
        with pytest.raises(ValueError):
            hand.draw(deck)


def test___contains__():
    deck = Deck()
    initial_cards = [deck.deal_top_card() for _ in range(5)]
    hand = Hand(initial_cards)

    for card in initial_cards:
        assert card in hand

    for card in deck._cards:
        assert card not in hand

    hand.play(3)

    for i, card in enumerate(initial_cards):
        if i == 3:
            continue
        assert card in hand

    for card in deck._cards:
        assert card not in hand

    for _ in range(4):
        hand.play(0)

    for card in initial_cards + deck._cards:
        assert card not in hand
