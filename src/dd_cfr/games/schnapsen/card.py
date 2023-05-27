"""
Defines the :obj:`Card` class.
"""

from .card_value import CardValue
from .suit import Suit


class Card:
    """
    Represents a playing card.
    """

    def __init__(self, suit: Suit, value: CardValue) -> None:
        """
        Construct a new instance.

        :param suit: The suit of the card.
        :param value: The card value.
        """

        self._suit = suit
        self._value = value

    def get_suit(self) -> Suit:
        """
        Return the card's suit.

        :return: Returns the card's suit.
        """

        return self._suit

    def get_card_value(self) -> CardValue:
        """
        Return the card value.

        :return: Returns the card value.
        """

        return self._value
