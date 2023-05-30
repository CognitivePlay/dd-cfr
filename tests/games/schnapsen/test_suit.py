from dd_cfr.games.schnapsen.suit import Suit


def test_cardinality():
    assert len(Suit) == 4


def test_uniqueness():
    for suit1 in list(Suit):
        for suit2 in list(Suit):
            # Would fail e.g. when Suit were converted to an IntEnum and some
            # enum members shared a common value:
            assert suit1 is suit2 or suit1 != suit2
