"""
Defines the :obj:`Card` class.
"""

import dataclasses

from .card_value import CardValue
from .suit import Suit


@dataclasses.dataclass
class Card:
    """
    Represents a playing card.
    """

    suit: Suit
    card_value: CardValue
