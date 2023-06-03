import random
import typing

import pytest

from dd_cfr.games.schnapsen import card, card_collection

# Tests for the :obj:`Deck` class:


def assert_all_cards_exist_once(list_of_cards: typing.List[card.Card]):
    all_cards = card_collection.Deck._get_list_of_all_cards()
    assert len(all_cards) == len(list_of_cards)

    for card in all_cards:
        found = False
        for other_card in list_of_cards:
            if card == other_card:
                found = True
                break
        assert found, card


def test_Deck___init__():
    deck_default_rng_1 = card_collection.Deck()
    deck_default_rng_2 = card_collection.Deck()
    deck_seeded_rng_1 = card_collection.Deck(random.Random(0))
    deck_seeded_rng_2 = card_collection.Deck(random.Random(0))

    assert_all_cards_exist_once(deck_default_rng_1._cards)
    assert_all_cards_exist_once(deck_default_rng_2._cards)
    assert_all_cards_exist_once(deck_seeded_rng_1._cards)
    assert_all_cards_exist_once(deck_seeded_rng_2._cards)

    assert deck_default_rng_1._cards != deck_default_rng_2._cards
    assert deck_default_rng_1._cards != deck_seeded_rng_1._cards
    assert deck_default_rng_1._cards != deck_seeded_rng_2._cards

    assert deck_seeded_rng_1._cards == deck_seeded_rng_2._cards


def test_Deck_get_maximum_number_of_cards():
    assert card_collection.Deck.get_maximum_number_of_cards() == len(card.Suit) * len(
        card.CardValue
    )


def test_Deck_get_number_of_cards():
    deck = card_collection.Deck()
    expected = deck.get_maximum_number_of_cards()

    for _ in range(deck.get_maximum_number_of_cards()):
        assert deck.get_number_of_cards() == expected
        deck.deal_top_card()
        expected -= 1

    assert deck.get_number_of_cards() == 0


def test_Deck_get_turn_up_card():
    deck = card_collection.Deck()
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


def test_Deck_deal_top_card():
    deck = card_collection.Deck()

    for i in range(deck.get_maximum_number_of_cards()):
        expected = deck._cards[0]
        assert deck.get_number_of_cards() == deck.get_maximum_number_of_cards() - i
        assert deck.deal_top_card() == expected

    assert deck.get_number_of_cards() == 0

    with pytest.raises(ValueError):
        deck.deal_top_card()


def test_Deck__get_list_of_all_cards():
    expected = []
    for suit in list(card.Suit):
        for value in list(card.CardValue):
            expected.append(card.Card(suit, value))

    assert len(expected) == 4 * 5
    assert expected == card_collection.Deck._get_list_of_all_cards()


# Tests for the :obj:`Hand` class:


def test_Hand___init__():
    for number_of_cards in range(10):
        deck = card_collection.Deck()

        if number_of_cards == 5:
            card_collection.Hand([deck.deal_top_card() for _ in range(number_of_cards)])
        else:
            with pytest.raises(ValueError):
                card_collection.Hand(
                    [deck.deal_top_card() for _ in range(number_of_cards)]
                )


def test_Hand_get_number_of_cards():
    deck = card_collection.Deck()
    hand = card_collection.Hand([deck.deal_top_card() for _ in range(5)])

    assert hand.get_number_of_cards() == 5


def test_Hand_get_card():
    deck = card_collection.Deck()
    initial_cards = [deck.deal_top_card() for _ in range(5)]
    hand = card_collection.Hand(initial_cards)

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


def test_Hand_play():
    deck = card_collection.Deck()
    initial_cards = [deck.deal_top_card() for _ in range(5)]
    hand = card_collection.Hand(initial_cards)

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


def test_Hand_draw():
    deck = card_collection.Deck()
    initial_cards = [deck.deal_top_card() for _ in range(5)]
    hand = card_collection.Hand(initial_cards)

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
    deck = card_collection.Deck()
    hand = card_collection.Hand(initial_cards)

    hand.play(0)
    hand.draw(deck)

    hand.play(0)
    for _ in range(4):
        hand.play(0)
        with pytest.raises(ValueError):
            hand.draw(deck)


def test_Hand___contains__():
    deck = card_collection.Deck()
    initial_cards = [deck.deal_top_card() for _ in range(5)]
    hand = card_collection.Hand(initial_cards)

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


# Tests for the :obj:`WonCards` class:


def test_won_cards_get_number_of_cards():
    won_cards = card_collection.WonCards()

    assert won_cards.get_number_of_cards() == 0

    won_cards.add_card(card.Card(card.Suit.HEARTS, card.CardValue.TEN))
    assert won_cards.get_number_of_cards() == 1

    won_cards.add_card(card.Card(card.Suit.HEARTS, card.CardValue.JACK))
    assert won_cards.get_number_of_cards() == 2


def test_won_cards_add_card():
    won_cards = card_collection.WonCards()

    won_cards.add_card(card.Card(card.Suit.HEARTS, card.CardValue.TEN))
    won_cards.add_card(card.Card(card.Suit.HEARTS, card.CardValue.JACK))

    with pytest.raises(ValueError):
        won_cards.add_card(card.Card(card.Suit.HEARTS, card.CardValue.JACK))

    won_cards.add_card(card.Card(card.Suit.DIAMONDS, card.CardValue.JACK))


def test_won_cards_get_number_of_points():
    won_cards = card_collection.WonCards()

    assert won_cards.get_number_of_points() == 0

    won_cards.add_card(card.Card(card.Suit.HEARTS, card.CardValue.TEN))
    assert won_cards.get_number_of_points() == card.CardValue.TEN.get_points()

    won_cards.add_card(card.Card(card.Suit.HEARTS, card.CardValue.JACK))
    assert (
        won_cards.get_number_of_points()
        == card.CardValue.TEN.get_points() + card.CardValue.JACK.get_points()
    )

    won_cards.add_card(card.Card(card.Suit.DIAMONDS, card.CardValue.JACK))
    assert (
        won_cards.get_number_of_points()
        == card.CardValue.TEN.get_points() + 2 * card.CardValue.JACK.get_points()
    )


def test_won_cards___contains__():
    won_cards = card_collection.WonCards()

    assert card.Card(card.Suit.HEARTS, card.CardValue.TEN) not in won_cards
    assert card.Card(card.Suit.HEARTS, card.CardValue.JACK) not in won_cards
    assert card.Card(card.Suit.DIAMONDS, card.CardValue.JACK) not in won_cards

    won_cards.add_card(card.Card(card.Suit.HEARTS, card.CardValue.TEN))
    assert card.Card(card.Suit.HEARTS, card.CardValue.TEN) in won_cards
    assert card.Card(card.Suit.HEARTS, card.CardValue.JACK) not in won_cards
    assert card.Card(card.Suit.DIAMONDS, card.CardValue.JACK) not in won_cards

    won_cards.add_card(card.Card(card.Suit.HEARTS, card.CardValue.JACK))
    assert card.Card(card.Suit.HEARTS, card.CardValue.TEN) in won_cards
    assert card.Card(card.Suit.HEARTS, card.CardValue.JACK) in won_cards
    assert card.Card(card.Suit.DIAMONDS, card.CardValue.JACK) not in won_cards

    won_cards.add_card(card.Card(card.Suit.DIAMONDS, card.CardValue.JACK))
    assert card.Card(card.Suit.HEARTS, card.CardValue.TEN) in won_cards
    assert card.Card(card.Suit.HEARTS, card.CardValue.JACK) in won_cards
    assert card.Card(card.Suit.DIAMONDS, card.CardValue.JACK) in won_cards
