from dd_cfr.games.schnapsen.card_value import CardValue


def test_cardinality():
    assert len(list(CardValue)) == 5


def test_uniqueness():
    for value1 in list(CardValue):
        for value2 in list(CardValue):
            # Would fail e.g. when Suit were converted to an IntEnum and some
            # enum members shared a common value:
            assert value1 is value2 or value1 != value2


def test_get_points():
    assert CardValue.ACE.get_points() == 11
    assert CardValue.TEN.get_points() == 10
    assert CardValue.KING.get_points() == 4
    assert CardValue.QUEEN.get_points() == 3
    assert CardValue.JACK.get_points() == 2


def test_ordering():
    for value1 in list(CardValue):
        for value2 in list(CardValue):
            if value1.get_points() < value2.get_points():
                assert value1 < value2
            elif value1.get_points() == value2.get_points():
                assert value1 <= value2
                assert value1 == value2
                assert value1 >= value2
            else:
                assert value1 > value2
