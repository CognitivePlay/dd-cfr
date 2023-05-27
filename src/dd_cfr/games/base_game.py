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
        pass

    @abc.abstractmethod
    def is_terminal(self) -> bool:
        pass

    @abc.abstractmethod
    def get_payoffs(self) -> List[float]:
        pass

    @abc.abstractmethod
    def get_legal_actions(self) -> Sequence[Action]:
        pass

    @abc.abstractmethod
    def get_chance_probabilities(self) -> Mapping[Action, float]:
        pass

    @abc.abstractmethod
    def get_active_player(self) -> int:
        pass

    @abc.abstractmethod
    def get_inactive_player(self) -> int:
        pass

    @abc.abstractmethod
    def child(self, action: Action) -> Game:
        pass
