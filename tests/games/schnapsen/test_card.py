from dd_cfr.games.schnapsen import card

# Tests for the :obj:`Suit` enum:


def test_Suit_cardinality():
    assert len(card.Suit) == 4


def test_Suit_uniqueness():
    for suit1 in list(card.Suit):
        for suit2 in list(card.Suit):
            # Would fail e.g. when Suit were converted to an IntEnum and some
            # enum members shared a common value:
            assert suit1 is suit2 or suit1 != suit2


def test_Suit_get_id():
    assert card.Suit.HEARTS.get_id() == 0
    assert card.Suit.DIAMONDS.get_id() == 1
    assert card.Suit.SPADES.get_id() == 2
    assert card.Suit.CLUBS.get_id() == 3


# Tests for the :obj:`Value` enum:


def test_Value_cardinality():
    assert len(list(card.Value)) == 5


def test_Value_uniqueness():
    for value1 in list(card.Value):
        for value2 in list(card.Value):
            # Would fail e.g. when Suit were converted to an IntEnum and some
            # enum members shared a common value:
            assert value1 is value2 or value1 != value2


def test_Value_get_points():
    assert card.Value.ACE.get_points() == 11
    assert card.Value.TEN.get_points() == 10
    assert card.Value.KING.get_points() == 4
    assert card.Value.QUEEN.get_points() == 3
    assert card.Value.JACK.get_points() == 2


def test_Value_get_id():
    assert card.Value.ACE.get_id() == 0
    assert card.Value.TEN.get_id() == 1
    assert card.Value.KING.get_id() == 2
    assert card.Value.QUEEN.get_id() == 3
    assert card.Value.JACK.get_id() == 4


def test_Value_ordering():
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


def test_Card_values():
    for suit in list(card.Suit):
        for value in list(card.Value):
            my_card = card.Card(suit, value)

            assert my_card.suit == suit
            assert my_card.value == value


def test_Card_get_name():
    assert card.Card(card.Suit.HEARTS, card.Value.ACE).get_name() == "Ace of Hearts"
    assert card.Card(card.Suit.HEARTS, card.Value.TEN).get_name() == "Ten of Hearts"
    assert card.Card(card.Suit.HEARTS, card.Value.KING).get_name() == "King of Hearts"
    assert card.Card(card.Suit.HEARTS, card.Value.QUEEN).get_name() == "Queen of Hearts"
    assert card.Card(card.Suit.HEARTS, card.Value.JACK).get_name() == "Jack of Hearts"

    assert card.Card(card.Suit.DIAMONDS, card.Value.ACE).get_name() == "Ace of Diamonds"
    assert card.Card(card.Suit.DIAMONDS, card.Value.TEN).get_name() == "Ten of Diamonds"
    assert (
        card.Card(card.Suit.DIAMONDS, card.Value.KING).get_name() == "King of Diamonds"
    )
    assert (
        card.Card(card.Suit.DIAMONDS, card.Value.QUEEN).get_name()
        == "Queen of Diamonds"
    )
    assert (
        card.Card(card.Suit.DIAMONDS, card.Value.JACK).get_name() == "Jack of Diamonds"
    )

    assert card.Card(card.Suit.SPADES, card.Value.ACE).get_name() == "Ace of Spades"
    assert card.Card(card.Suit.SPADES, card.Value.TEN).get_name() == "Ten of Spades"
    assert card.Card(card.Suit.SPADES, card.Value.KING).get_name() == "King of Spades"
    assert card.Card(card.Suit.SPADES, card.Value.QUEEN).get_name() == "Queen of Spades"
    assert card.Card(card.Suit.SPADES, card.Value.JACK).get_name() == "Jack of Spades"

    assert card.Card(card.Suit.CLUBS, card.Value.ACE).get_name() == "Ace of Clubs"
    assert card.Card(card.Suit.CLUBS, card.Value.TEN).get_name() == "Ten of Clubs"
    assert card.Card(card.Suit.CLUBS, card.Value.KING).get_name() == "King of Clubs"
    assert card.Card(card.Suit.CLUBS, card.Value.QUEEN).get_name() == "Queen of Clubs"
    assert card.Card(card.Suit.CLUBS, card.Value.JACK).get_name() == "Jack of Clubs"


def test_Card_get_id():
    assert card.Card(card.Suit.HEARTS, card.Value.ACE).get_id() == 0
    assert card.Card(card.Suit.HEARTS, card.Value.TEN).get_id() == 1
    assert card.Card(card.Suit.HEARTS, card.Value.KING).get_id() == 2
    assert card.Card(card.Suit.HEARTS, card.Value.QUEEN).get_id() == 3
    assert card.Card(card.Suit.HEARTS, card.Value.JACK).get_id() == 4

    assert card.Card(card.Suit.DIAMONDS, card.Value.ACE).get_id() == 5
    assert card.Card(card.Suit.DIAMONDS, card.Value.TEN).get_id() == 6
    assert card.Card(card.Suit.DIAMONDS, card.Value.KING).get_id() == 7
    assert card.Card(card.Suit.DIAMONDS, card.Value.QUEEN).get_id() == 8
    assert card.Card(card.Suit.DIAMONDS, card.Value.JACK).get_id() == 9

    assert card.Card(card.Suit.SPADES, card.Value.ACE).get_id() == 10
    assert card.Card(card.Suit.SPADES, card.Value.TEN).get_id() == 11
    assert card.Card(card.Suit.SPADES, card.Value.KING).get_id() == 12
    assert card.Card(card.Suit.SPADES, card.Value.QUEEN).get_id() == 13
    assert card.Card(card.Suit.SPADES, card.Value.JACK).get_id() == 14

    assert card.Card(card.Suit.CLUBS, card.Value.ACE).get_id() == 15
    assert card.Card(card.Suit.CLUBS, card.Value.TEN).get_id() == 16
    assert card.Card(card.Suit.CLUBS, card.Value.KING).get_id() == 17
    assert card.Card(card.Suit.CLUBS, card.Value.QUEEN).get_id() == 18
    assert card.Card(card.Suit.CLUBS, card.Value.JACK).get_id() == 19


def test_Card___eq__():
    ace_of_spades = card.Card(card.Suit.SPADES, card.Value.ACE)
    assert ace_of_spades == ace_of_spades

    assert ace_of_spades == card.Card(card.Suit.SPADES, card.Value.ACE)

    assert not ace_of_spades == (card.Suit.SPADES, card.Value.ACE)
    assert ace_of_spades != (card.Suit.SPADES, card.Value.ACE)

    assert not ace_of_spades == card.Card(card.Suit.SPADES, card.Value.KING)
    assert ace_of_spades != card.Card(card.Suit.SPADES, card.Value.KING)

    assert not ace_of_spades == (card.Suit.HEARTS, card.Value.ACE)
    assert ace_of_spades != (card.Suit.HEARTS, card.Value.ACE)
