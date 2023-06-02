"""Defines the :obj:`Deck` class."""

import random
import typing

from dd_cfr.games.schnapsen.card import Card
from dd_cfr.games.schnapsen.card_value import CardValue
from dd_cfr.games.schnapsen.suit import Suit


class Deck:
    """Represents a playing deck (complete set of cards before shuffling, and the talon
    and turn-up card afterwards until they are drawn too).
    """

    def __init__(self, rng: typing.Optional[random.Random] = None) -> None:
        """Construct a new, shuffled deck of Schnapsen cards.

        :param rng: A random number generator, or ``None`` to use the global state of
            the :obj:`random` module.
        """

        self._cards = self._get_list_of_all_cards()
        (rng or random.Random()).shuffle(self._cards)

    @staticmethod
    def get_maximum_number_of_cards() -> int:
        """Return the maximum number of cards in a game, i.e., the number of cards in a
        deck before it is dealt.

        :return: The maximum number of cards in a game of Schnapsen.
        """

        return len(Suit) * len(CardValue)

    def get_number_of_cards(self) -> int:
        """Return the number of cards left in the deck, including the turn-up card.

        :return: Number of cards left in the stack.
        """

        return len(self._cards)

    def get_turn_up_card(self) -> Card:
        """Return the turn-up card, without removing it from the deck.

        :raises ValueError: Raises if no cards are left in the deck.
        :return: The turn-up card.
        """

        if not self._cards:
            raise ValueError("No cards left in deck to deal")

        return self._cards[-1]

    def deal_top_card(self) -> Card:
        """Return the deck's top card (possibly the turn-up card), and remove it from
        the stack.

        :raises ValueError: Raises if no cards are left in the deck.
        :return: The top card.
        """

        if not self._cards:
            raise ValueError("No cards left in deck to deal")

        return self._cards.pop(0)

    @staticmethod
    def _get_list_of_all_cards() -> typing.List[Card]:
        """Return a list containing all Schnapsen cards, each appearing exactly once.

        :return: List of all cards, ordered first by suit, then by value.
        """

        return [Card(suit, value) for suit in Suit for value in CardValue]
