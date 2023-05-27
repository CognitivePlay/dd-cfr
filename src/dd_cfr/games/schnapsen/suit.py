"""
Defines the :obj:`Suit` class.
"""

import enum


@enum.unique
class Suit(enum.Enum):
    """
    Enumeration of card suits, i.e., ``Hearts``, ``Diamonds``, ``Spades``, and
    ``Clubs``.
    """

    #: The suit ``Hearts`` (both in French and Double German pattern)
    HEARTS = enum.auto()

    #: The suit ``Diamonds`` (in French pattern; ``Bells`` in Double German)
    DIAMONDS = enum.auto()

    #: The suit ``Spades`` (in French pattern; ``Leaves`` in Double German)
    SPADES = enum.auto()

    #: The suit ``Clubs`` (in French pattern; ``Acorns`` in Double German)
    CLUBS = enum.auto()
