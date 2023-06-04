"""Defines the :obj:`Deck`, :obj:`Hand`, and :obj:`WonCards` classes."""

import random
import typing

from dd_cfr.games.schnapsen import card


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

        return len(card.Suit) * len(card.Value)

    def get_number_of_cards(self) -> int:
        """Return the number of cards left in the deck, including the turn-up card.

        :return: Number of cards left in the stack.
        """

        return len(self._cards)

    def get_turn_up_card(self) -> card.Card:
        """Return the turn-up card, without removing it from the deck.

        :raises ValueError: Raises if no cards are left in the deck.
        :return: The turn-up card.
        """

        if not self._cards:
            raise ValueError("No cards left in deck to deal")

        return self._cards[-1]

    def deal_top_card(self) -> card.Card:
        """Return the deck's top card (possibly the turn-up card), and remove it from
        the stack.

        :raises ValueError: Raises if no cards are left in the deck.
        :return: The top card.
        """

        if not self._cards:
            raise ValueError("No cards left in deck to deal")

        return self._cards.pop(0)

    @staticmethod
    def _get_list_of_all_cards() -> typing.List[card.Card]:
        """Return a list containing all Schnapsen cards, each appearing exactly once.

        :return: List of all cards, ordered first by suit, then by value.
        """

        return [card.Card(suit, value) for suit in card.Suit for value in card.Value]


class Hand:
    """Represents a player's hand, i.e., up to five cards."""

    def __init__(self, cards: typing.List[card.Card]) -> None:
        """Construct a hand from a set of given cards.

        :param cards: A list of five cards (contents will be copied).
        :raises ValueError: Raises if :obj:`cards` is not of length ``5``.
        """

        if not len(cards) == 5:
            raise ValueError("{len(cards)} cards were given instead of 5 expected.")

        self._cards = cards[:]

    def get_number_of_cards(self) -> int:
        """Return the number of cards in the hand.

        :return: Number of cards in the hand.
        """

        return len(self._cards)

    def get_card(self, index: int) -> card.Card:
        """Return the card at the given index without removing it from the hand.

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

    def play(self, index: int) -> card.Card:
        """Play the card at the given index, i.e., remove it from the hand and return
        it.

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
        """Draw the top card of the deck, removing it there and adding it to the hand.

        :param deck: The deck to draw the top card from.
        :raises ValueError: Raises if the hand does not contain exactly 4 cards.
        :raises ValueError: Raises if the deck does not contain further cards.
        """

        if not self.get_number_of_cards() == 4:
            raise ValueError("Cannot draw a card unless to replenish the fifth card.")
        if deck.get_number_of_cards() == 0:
            raise ValueError("Cannot draw from an empty deck.")

        self._cards.append(deck.deal_top_card())

    def __contains__(self, my_card: card.Card) -> bool:
        """Return whether the given card is in this hand.

        :param my_card: The card to check for.
        :return: ``True`` if the card is in the hand, ``False`` otherwise.
        """

        return my_card in self._cards


class WonCards:
    """Represents cards won by a player."""

    def __init__(self) -> None:
        """Construct an empty list of won cards."""

        self._cards: typing.List[card.Card] = []

    def get_number_of_cards(self) -> int:
        """Return the number of cards won.

        :return: Number of cards won.
        """

        return len(self._cards)

    def add_card(self, my_card: card.Card) -> None:
        """Add the given card to the won cards.

        :param my_card: The card to add.
        :raises ValueError: Raises if the card is already in the list of won cards.
        """

        if my_card in self:
            raise ValueError(f"Duplicate card: {my_card}")

        self._cards.append(my_card)

    def get_number_of_points(self) -> int:
        """Return the number of points by adding up all the point values of the cards in
        this collection of won cards.

        :return: The sum of the cards' point values.
        """

        return sum(card.value.get_points() for card in self._cards)

    def __contains__(self, my_card: card.Card) -> bool:
        """Return whether the given card is in this hand.

        :param my_card: The card to check for.
        :return: ``True`` if the card is in the hand, ``False`` otherwise.
        """

        return my_card in self._cards
