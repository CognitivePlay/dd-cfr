from dd_cfr.games.schnapsen import card

# Tests for the :obj:`Suit` enum:


def test_suit_cardinality():
    assert len(card.Suit) == 4


def test_suit_uniqueness():
    for suit1 in list(card.Suit):
        for suit2 in list(card.Suit):
            # Would fail e.g. when Suit were converted to an IntEnum and some
            # enum members shared a common value:
            assert suit1 is suit2 or suit1 != suit2


# Tests for the :obj:`Value` enum:


def test_value_cardinality():
    assert len(list(card.Value)) == 5


def test_value_uniqueness():
    for value1 in list(card.Value):
        for value2 in list(card.Value):
            # Would fail e.g. when Suit were converted to an IntEnum and some
            # enum members shared a common value:
            assert value1 is value2 or value1 != value2


def test_value_get_points():
    assert card.Value.ACE.get_points() == 11
    assert card.Value.TEN.get_points() == 10
    assert card.Value.KING.get_points() == 4
    assert card.Value.QUEEN.get_points() == 3
    assert card.Value.JACK.get_points() == 2


def test_value_ordering():
    for value1 in list(card.Value):
        for value2 in list(card.Value):
            if value1.get_points() < value2.get_points():
                assert value1 < value2
            elif value1.get_points() == value2.get_points():
                assert value1 <= value2
                assert value1 == value2
                assert value1 >= value2
            else:
                assert value1 > value2


# Tests for the :obj:`Card` class:


def test_card_values():
    for suit in list(card.Suit):
        for value in list(card.Value):
            my_card = card.Card(suit, value)

            assert my_card.suit == suit
            assert my_card.card_value == value


def test_card___eq__():
    ace_of_spades = card.Card(card.Suit.SPADES, card.Value.ACE)
    assert ace_of_spades == ace_of_spades

    assert ace_of_spades == card.Card(card.Suit.SPADES, card.Value.ACE)

    assert not ace_of_spades == (card.Suit.SPADES, card.Value.ACE)
    assert ace_of_spades != (card.Suit.SPADES, card.Value.ACE)

    assert not ace_of_spades == card.Card(card.Suit.SPADES, card.Value.KING)
    assert ace_of_spades != card.Card(card.Suit.SPADES, card.Value.KING)

    assert not ace_of_spades == (card.Suit.HEARTS, card.Value.ACE)
    assert ace_of_spades != (card.Suit.HEARTS, card.Value.ACE)
