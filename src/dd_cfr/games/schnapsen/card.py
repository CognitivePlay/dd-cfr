"""Defines the :obj:`Suit`, :obj:`Value`, and :obj:`Card` classes."""

from __future__ import annotations

import dataclasses
import enum
import functools


@enum.unique
class Suit(enum.Enum):
    """Enumeration of card suits, i.e., ``Hearts``, ``Diamonds``, ``Spades``, and
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


@functools.total_ordering
@enum.unique
class Value(enum.Enum):
    """Enumeration of card values, i.e., ``Ace``, ``Ten``, ``King``, ``Queen``, and
    ``Jack``, with their respective points values.
    """

    #: The ``Ace`` value (in French pattern; ``Deuce`` or ``Sow`` in Double German)
    ACE = 11

    #: The ``Ten`` value (in French and Double German pattern)
    TEN = 10

    #: The ``King`` value (in French and Double German pattern)
    KING = 4

    #: The ``Queen`` value (in French pattern; ``Ober`` or ``Manderl`` in Double German)
    QUEEN = 3

    #: The ``Jack`` value (in French pattern; ``Unter`` or ``Bauer`` in Double German)
    JACK = 2

    def get_points(self) -> int:
        """Return the card's points value.

        :returns: Returns the card's points value.
        """

        return self.value

    def __lt__(self, rhs: Value) -> bool:
        """Return whether this instance's card value is less than the right-hand-side's.

        :param rhs: The right-hand-side value.
        :return: Returns whether this instance's card value is less than :obj:`rhs`'s.
        """
        return self.value < rhs.value


@dataclasses.dataclass
class Card:
    """Represents a playing card."""

    suit: Suit
    card_value: Value
