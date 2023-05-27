"""
Defines the :obj:`Hand` class.
"""

import typing

from .card import Card
from .deck import Deck


class Hand:
    """
    Represents a player's hand, i.e., up to five cards.
    """

    def __init__(self, cards: typing.List[Card]) -> None:
        """
        Construct a hand from a set of given cards.

        :param cards: A list of five cards (contents will be copied).
        :raises ValueError: Raises if :obj:`cards` is not of length ``5``.
        """

        if not len(cards) == 5:
            raise ValueError("{len(cards)} cards were given instead of 5 expected.")

        self._cards = cards[:]

    def get_number_of_cards(self) -> int:
        """
        Return the number of cards in the hand.

        :return: Number of cards in the hand.
        """

        return len(self._cards)

    def get_card(self, index: int) -> Card:
        """
        Return the card at the given index without removing it from the hand.

        :param index: The index of the card to play, in the range
            ``[0, get_number_of_cards())``.
        :raises ValueError: Raises if ``get_number_of_cards() == 0``.
        :raises IndexError: Raises if the index is not in the range
            ``[0, get_number_of_cards())``.
        :return: The card at the given index.
        """

        if self.get_number_of_cards() == 0:
            raise ValueError("Cannot get cards from an empty hand.")
        if index not in range(self.get_number_of_cards()):
            raise IndexError(f"Invalid index for hand: {index}")

        return self._cards[index]

    def play(self, index: int) -> Card:
        """
        Play the card at the given index, i.e., remove it from the hand and return it.

        :param index: The index of the card to play, in the range
            ``[0, get_number_of_cards())``.
        :raises ValueError: Raises if ``get_number_of_cards() == 0``.
        :raises IndexError: Raises if the index is not in the range
            ``[0, get_number_of_cards())``.
        :return: The removed card.
        """

        if self.get_number_of_cards() == 0:
            raise ValueError("Cannot play an empty hand.")
        if index not in range(self.get_number_of_cards()):
            raise IndexError(f"Invalid index for hand: {index}")

        return self._cards.pop(index)

    def draw(self, deck: Deck) -> None:
        """
        Draw the top card of the deck, removing it there and adding it to the hand.

        :param deck: The deck to draw the top card from.
        :raises ValueError: Raises if the hand does not contain exactly 4 cards.
        :raises ValueError: Raises if the deck does not contain further cards.
        """

        if not self.get_number_of_cards() == 4:
            raise ValueError("Cannot draw a card unless to replenish the fifth card.")
        if deck.get_number_of_cards() == 0:
            raise ValueError("Cannot draw from an empty deck.")

        self._cards.append(deck.deal_top_card())

    def __contains__(self, card: Card) -> bool:
        """
        Return whether the given ``card`` is in this hand.

        :param card: The card to check for.
        :return: ``True`` if the card is in the hand, ``False`` otherwise.
        """

        for i in range(self.get_number_of_cards()):
            if self.get_card(i) == card:
                return True
        return False
