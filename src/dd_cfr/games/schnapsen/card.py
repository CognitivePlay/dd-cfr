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

    def get_id(self) -> int:
        """Return a numeric identifier for the suit, in the range ``[0, 4)``.

        :return: The unique suit identifier.
        """

        # Merely using `self.HEARTS` below would provoke a `mypy` error.
        # Alternative: Use `Suit.HEARTS`, but that would needlessly make the member
        # function assume what the name of its class is.
        id_dict = {
            self.__class__.HEARTS: 0,
            self.__class__.DIAMONDS: 1,
            self.__class__.SPADES: 2,
            self.__class__.CLUBS: 3,
        }

        return id_dict[self]


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

        :return: The card's points value.
        """

        return self.value

    def get_id(self) -> int:
        """Return a numeric identifier for the card value, in the range ``[0, 5)``.

        :return: The unique card value identifier.
        """

        # Merely using `self.ACE` below would provoke a `mypy` error.
        # Alternative: Use `Value.ACE`, but that would needlessly make the member
        # function assume what the name of its class is.
        id_dict = {
            self.__class__.ACE: 0,
            self.__class__.TEN: 1,
            self.__class__.KING: 2,
            self.__class__.QUEEN: 3,
            self.__class__.JACK: 4,
        }

        return id_dict[self]

    def __lt__(self, other: Value) -> bool:
        """Return whether this instance's card value is less than the other one.

        :param other: The value to compare to.
        :return: Whether this instance's card value is less than :obj:`other`'s.
        """
        return self.value < other.value


@dataclasses.dataclass
class Card:
    """Represents a playing card."""

    suit: Suit
    value: Value

    def get_name(self) -> str:
        """Return the French-pattern name of the card.

        :return: The card's name in French-pattern nomenclature.
        """

        return self.value.name.title() + " of " + self.suit.name.title()

    def get_id(self) -> int:
        """Return a numeric identifier for the card, in the range ``[0, 20)``, where
        ``20`` is the total number of cards in a game of Schnapsen.

        :return: Unique numeric identifier for the card.
        """

        return 5 * self.suit.get_id() + self.value.get_id()
