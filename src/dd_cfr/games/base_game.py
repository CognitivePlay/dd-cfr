"""Abstract classes for implementing games."""

from __future__ import annotations

import abc
import enum
from typing import List, Mapping, Sequence


class Action(enum.Enum):
    pass


class Game(abc.ABC):
    """Abstract class for implementing games."""

    @abc.abstractmethod
    def get_state(self) -> str:
        """
        Returns the state from the perspective of the currently active player.
        """

    @abc.abstractmethod
    def is_terminal(self) -> bool:
        """
        Returns whether the current state is terminal.
        """

    @abc.abstractmethod
    def get_payoffs(self) -> List[float]:
        """
        Returns the payoffs for all players in order.
        """

    @abc.abstractmethod
    def get_legal_actions(self) -> Sequence[Action]:
        """
        Returns the legal actions for the currently active (possibly chance) player.
        """

    @abc.abstractmethod
    def get_chance_probabilities(self) -> Mapping[Action, float]:
        """
        Returns the chance probabilities, only valid when the chance player is active.
        """

    @abc.abstractmethod
    def get_active_player(self) -> int:
        """
        Returns the currently active player.
        """

    @abc.abstractmethod
    def child(self, action: Action) -> Game:
        """
        Returns a copy of the current game state with the given action applied.
        """

    def _get_other_player(self, player: int) -> int:
        return (player + 1) % 2

    def get_inactive_player(self) -> int:
        """
        Returns the currently inactive player.
        """
        return self._get_other_player(self.get_active_player())
