"""Kuhn poker implementation."""
from __future__ import annotations

import copy
import dataclasses
from typing import List, Mapping, Optional, Sequence

from dd_cfr import common
from dd_cfr.games import base_game


class Action(base_game.Action):
    """All available actions to the players."""

    CHECK = 0
    BET = 1
    CALL = 2
    FOLD = 3


class ChanceAction(base_game.Action):
    """All available actions to the chance player."""

    JACK = 0
    QUEEN = 1
    KING = 2


@dataclasses.dataclass
class PlayerAction:
    """Holds the player and action combination."""

    player: int
    action: Action


class KuhnPoker(base_game.Game):
    """KuhnPoker game."""

    def __init__(
        self,
        cards: Optional[List[ChanceAction]] = None,
        history: Optional[List[PlayerAction]] = None,
    ) -> None:
        """Initialize KuhnPoker class.

        :param cards: Optional current cards, defaults to None.
        :param history: Optional current history, defaults to None.
        """
        self._cards = cards if cards is not None else []
        self._history = history if history is not None else []

    def _get_winner(self) -> int:
        if self._history[-1].action == Action.FOLD:
            return self._get_other_player(self._history[-1].player)

        return max(enumerate(self._cards), key=lambda x: x[1].value)[0]

    def _get_winning_amount(self) -> int:
        if Action.CALL in [pa.action for pa in self._history]:
            return 2
        return 1

    def _get_formatted_card(self, card: ChanceAction) -> str:
        return card.name

    def _get_formatted_history(self) -> str:
        return ", ".join(str(pa.action.name) for pa in self._history)

    def get_state(self) -> str:
        """Return the state from the perspective of the currently active player.

        :return: The state from the perspective of the currently active player.
        """
        # Active player was not dealt a card yet.
        if self.get_active_player() >= len(self._cards):  # pragma: no cover
            return ""

        history = self._get_formatted_history()

        return self._get_formatted_card(self._cards[self.get_active_player()]) + (
            "|" + history if history else ""
        )

    def is_terminal(self) -> bool:
        """Return whether the current state is terminal.

        :return: Whether the current state is terminal.
        """
        return len(self._history) == 3 or (
            len(self._history) == 2 and self._history[-1].action != Action.BET
        )

    def get_payoffs(self) -> List[float]:
        """Return the payoffs for all players in order.

        :return: The payoffs for all players in order.
        """
        winner = self._get_winner()
        winning_amount = self._get_winning_amount()
        payoffs = [0.0, 0.0]

        payoffs[winner] = winning_amount
        payoffs[self._get_other_player(winner)] = -winning_amount

        return payoffs

    def get_legal_actions(self) -> Sequence[Action]:
        """Return the legal actions for the active (possibly chance) player.

        :raises ValueError: If legal actions are retrieved for an  impossible state.
        :return: The legal actions for the active player.
        """
        if not self._history or self._history[-1].action == Action.CHECK:
            return [Action.CHECK, Action.BET]

        if self._history[-1].action == Action.BET:
            return [Action.CALL, Action.FOLD]

        raise ValueError(
            f"Should not reach this state after {self._history[-1]}"
        )  # pragma: no cover

    def get_chance_probabilities(self) -> Mapping[base_game.Action, float]:
        """Return chance probabilities, only valid when the chance player is active.

        :raises ValueError: If the active player is not the chance player
        :return: The chance probabilities for the current state.
        """
        if self.get_active_player() != common.CHANCE_PLAYER:
            raise ValueError(
                "Should only call get_chance_probabilities when the chance player is"
                " active."
            )  # pragma: no cover

        cards = sorted((set(ChanceAction) - set(self._cards)), key=lambda x: x.value)
        return {card: 1 / len(cards) for card in cards}

    def get_active_player(self) -> int:
        """Return the currently active player.

        :return: The currently active player.
        """
        if len(self._cards) < 2:
            return common.CHANCE_PLAYER

        if not self._history:
            return 0

        return self._get_other_player(self._history[-1].player)

    def child(self, action: base_game.Action) -> KuhnPoker:
        """Return a copy of the current game state with the given action applied.

        :param action: The action to apply.
        :return: A copy of the current game with the given action applied.
        """

        new_cards = copy.deepcopy(self._cards)
        new_history = copy.deepcopy(self._history)

        if self.get_active_player() == common.CHANCE_PLAYER:
            new_cards.append(ChanceAction(action))
        else:
            new_history.append(PlayerAction(self.get_active_player(), Action(action)))

        return KuhnPoker(new_cards, new_history)
