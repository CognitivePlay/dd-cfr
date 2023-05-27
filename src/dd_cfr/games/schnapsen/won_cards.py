"""
Defines the :obj:`WonCards` class.
"""

import typing

from .card import Card


class WonCards:
    """
    Represents cards won by a player.
    """

    def __init__(self) -> None:
        """
        Construct an empty list of won cards.
        """

        self._cards: typing.List[Card] = []

    def get_number_of_cards(self) -> int:
        """
        Return the number of cards won.

        :return: Number of cards won.
        """

        return len(self._cards)

    def add_card(self, card: Card) -> None:
        """
        Add the given card to the won cards.

        :param card: The card to add.
        :raises ValueError: Raises if the card is already in the list of won cards.
        """

        if card in self:
            raise ValueError(f"Duplicate card: {card}")

        self._cards.append(card)

    def get_number_of_points(self) -> int:
        """
        Return the number of points by adding up all the point values of the cards in
        this collection of won cards.

        :return: The sum of the cards' point values.
        """

        return sum(card.card_value.get_points() for card in self._cards)

    def __contains__(self, card: Card) -> bool:
        """
        Return whether the given ``card`` is in this hand.

        :param card: The card to check for.
        :return: ``True`` if the card is in the hand, ``False`` otherwise.
        """

        return card in self._cards
