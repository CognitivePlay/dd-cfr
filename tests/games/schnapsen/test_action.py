from dd_cfr.games.schnapsen import action


# Tests for the :obj:`PlayerAction` enum:


def test_PlayerAction_cardinality():
    assert len(action.PlayerAction) == 26


def test_PlayerAction_uniqueness():
    for a1 in list(action.PlayerAction):
        for a2 in list(action.PlayerAction):
            assert a1 is a2 or a1 != a2


def test_PlayerAction_values():
    assert action.PlayerAction.ACE_OF_HEARTS == 0
    assert action.PlayerAction.TEN_OF_HEARTS == 1
    assert action.PlayerAction.KING_OF_HEARTS == 2
    assert action.PlayerAction.QUEEN_OF_HEARTS == 3
    assert action.PlayerAction.JACK_OF_HEARTS == 4

    assert action.PlayerAction.ACE_OF_DIAMONDS == 5
    assert action.PlayerAction.TEN_OF_DIAMONDS == 6
    assert action.PlayerAction.KING_OF_DIAMONDS == 7
    assert action.PlayerAction.QUEEN_OF_DIAMONDS == 8
    assert action.PlayerAction.JACK_OF_DIAMONDS == 9

    assert action.PlayerAction.ACE_OF_SPADES == 10
    assert action.PlayerAction.TEN_OF_SPADES == 11
    assert action.PlayerAction.KING_OF_SPADES == 12
    assert action.PlayerAction.QUEEN_OF_SPADES == 13
    assert action.PlayerAction.JACK_OF_SPADES == 14

    assert action.PlayerAction.ACE_OF_CLUBS == 15
    assert action.PlayerAction.TEN_OF_CLUBS == 16
    assert action.PlayerAction.KING_OF_CLUBS == 17
    assert action.PlayerAction.QUEEN_OF_CLUBS == 18
    assert action.PlayerAction.JACK_OF_CLUBS == 19

    assert action.PlayerAction.EXCHANGE_TURN_UP == 20
    assert action.PlayerAction.CLOSE_TALON == 21
    assert action.PlayerAction.MELD_HEARTS_MARRIAGE == 22
    assert action.PlayerAction.MELD_DIAMONDS_MARRIAGE == 23
    assert action.PlayerAction.MELD_SPADES_MARRIAGE == 24
    assert action.PlayerAction.MELD_CLUBS_MARRIAGE == 25
