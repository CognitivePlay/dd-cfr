"""Abstract classes for implementing games."""
from __future__ import annotations

import abc
import enum
from typing import Sequence

from dd_cfr import common


class Action(enum.Enum):
    """The set of actions available to the (possibly chance) players."""


class Game(abc.ABC):
    """Abstract class for implementing games."""

    @abc.abstractmethod
    def get_state(self) -> str:
        """Return the state from the perspective of the currently active player."""

    @abc.abstractmethod
    def is_terminal(self) -> bool:
        """Return whether the current state is terminal."""

    @abc.abstractmethod
    def get_payoffs(self) -> list[float]:
        """Return the payoffs for players 1 and 2 in order."""

    @abc.abstractmethod
    def get_legal_actions(self) -> Sequence[Action]:
        """Return the legal actions for the active (possibly chance) player."""

    @abc.abstractmethod
    def get_chance_probabilities(self) -> dict[Action, float]:
        """Return chance probabilities, only valid when the chance player is active."""

    @abc.abstractmethod
    def get_active_player(self) -> int:
        """Return the currently active player."""

    @abc.abstractmethod
    def child(self, action: Action) -> Game:
        """Return a copy of the current game state with the given action applied.

        :param action: The action to apply.
        """

    def _get_other_player(self, player: int) -> int:
        return (player + 1) % 2

    def get_inactive_player(self) -> int:
        """Return the currently inactive player.

        :return: The inactive player.
        :raises ValueError: If the currently active player is the chance player.
        """
        active_player = self.get_active_player()
        if active_player == common.CHANCE_PLAYER:  # pragma: no cover
            raise ValueError(
                "get_inactive_player should not be called when the chance player is"
                " active."
            )

        return self._get_other_player(active_player)
