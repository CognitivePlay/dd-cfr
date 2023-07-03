"""Defines the :obj:`Action` enumeration."""

import enum

from dd_cfr.games.schnapsen import card_collection

# Below enum has mypy type checking disabled due to dynamically-generated member names
# being unsupported (see https://github.com/python/mypy/issues/4865).
PlayerAction = enum.IntEnum(  # type: ignore
    "PlayerAction",
    {
        **{
            card.get_name().replace(" ", "_").upper(): card.get_id()
            for card in card_collection.Deck.get_list_of_all_cards()
        },
        **{
            name: 20 + id
            for id, name in enumerate(
                [
                    "EXCHANGE_TURN_UP",  # Exchange the Trump Jack for the turn-up card.
                    "CLOSE_TALON",  # Close the talon.
                    "MELD_HEARTS_MARRIAGE",  # Announce a King-Queen pair of Hearts.
                    "MELD_DIAMONDS_MARRIAGE",  # Announce a King-Queen pair of Diamonds.
                    "MELD_SPADES_MARRIAGE",  # Announce a King-Queen pair of Spades.
                    "MELD_CLUBS_MARRIAGE",  # Announce a King-Queen pair of Clubs.
                ]
            )
        },
    },
)
