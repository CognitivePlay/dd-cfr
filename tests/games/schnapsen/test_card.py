"""Tests the ``card`` module."""

# pragma pylint: disable=comparison-with-itself

from dd_cfr.games.schnapsen import card


class TestSuit:
    def test_cardinality(self):
        assert len(card.Suit) == 4

    def test_uniqueness(self):
        for suit1 in list(card.Suit):
            for suit2 in list(card.Suit):
                # Would fail e.g. when Suit were converted to an IntEnum and some
                # enum members shared a common value:
                assert suit1 is suit2 or suit1 != suit2


class TestValue:
    def test_cardinality(self):
        assert len(list(card.Value)) == 5

    def test_uniqueness(self):
        for value1 in list(card.Value):
            for value2 in list(card.Value):
                # Would fail e.g. when Suit were converted to an IntEnum and some
                # enum members shared a common value:
                assert value1 is value2 or value1 != value2

    def test_get_points(self):
        assert card.Value.ACE.get_points() == 11
        assert card.Value.TEN.get_points() == 10
        assert card.Value.KING.get_points() == 4
        assert card.Value.QUEEN.get_points() == 3
        assert card.Value.JACK.get_points() == 2

    def test_ordering(self):
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


class TestCard:
    def test__values(self):
        for suit in list(card.Suit):
            for value in list(card.Value):
                my_card = card.Card(suit, value)

                assert my_card.suit == suit
                assert my_card.value == value

    def test____eq__(self):
        ace_of_spades = card.Card(card.Suit.SPADES, card.Value.ACE)
        assert ace_of_spades == ace_of_spades

        assert ace_of_spades == card.Card(card.Suit.SPADES, card.Value.ACE)
        assert ace_of_spades != (card.Suit.SPADES, card.Value.ACE)
        assert ace_of_spades != card.Card(card.Suit.SPADES, card.Value.KING)
        assert ace_of_spades != (card.Suit.HEARTS, card.Value.ACE)
