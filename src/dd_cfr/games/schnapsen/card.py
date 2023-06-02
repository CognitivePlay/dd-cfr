"""Defines the :obj:`Card` class."""

import dataclasses

from dd_cfr.games.schnapsen.card_value import CardValue
from dd_cfr.games.schnapsen.suit import Suit


@dataclasses.dataclass
class Card:
    """Represents a playing card."""

    suit: Suit
    card_value: CardValue
