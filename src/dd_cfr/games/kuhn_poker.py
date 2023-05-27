"""Kuhn poker implementation."""

from __future__ import annotations

import copy
import dataclasses
from typing import List, Mapping, Optional, Sequence

from dd_cfr import common
from dd_cfr.games import base_game


class Action(base_game.Action):
    CHECK = 0
    BET = 1
    CALL = 2
    FOLD = 3


class ChanceAction(base_game.Action):
    JACK = 0
    QUEEN = 1
    KING = 2


@dataclasses.dataclass
class PlayerAction:
    player: int
    action: Action


class KuhnPoker(base_game.Game):
    """KuhnPoker Game."""

    def __init__(
        self,
        cards: Optional[List[ChanceAction]] = None,
        history: Optional[List[PlayerAction]] = None,
    ) -> None:
        """
        Initialize KuhnPoker class

        :param cards: Optional current cards, defaults to None.
        :param history: Optional current history, defaults to None.
        """
        if cards is None:
            cards = []
        if history is None:
            history = []

        self._cards = cards
        self._history = history

    def _get_other_player(self, player: int) -> int:
        return (player + 1) % 2

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
        if len(self._cards) < 2:
            return ""

        history = self._get_formatted_history()

        return self._get_formatted_card(self._cards[self.get_active_player()]) + (
            "|" + history if history else ""
        )

    def is_terminal(self) -> bool:
        return len(self._history) == 3 or (
            len(self._history) == 2 and self._history[-1].action != Action.BET
        )

    def get_payoffs(self) -> List[float]:
        winner = self._get_winner()
        winning_amount = self._get_winning_amount()
        payoffs = [0.0, 0.0]

        payoffs[winner] = winning_amount
        payoffs[self._get_other_player(winner)] = -winning_amount

        return payoffs

    def get_legal_actions(self) -> Sequence[Action]:
        if not self._history or self._history[-1].action == Action.CHECK:
            return [Action.CHECK, Action.BET]

        if self._history[-1].action == Action.BET:
            return [Action.CALL, Action.FOLD]

        raise ValueError(f"Should not reach this state after {self._history[-1]}")

    def get_chance_probabilities(self) -> Mapping[base_game.Action, float]:
        if self.get_active_player() != common.CHANCE_PLAYER:
            raise ValueError(
                "Should only call get_chance_probabilities when the chance player is"
                " active."
            )

        cards = set(ChanceAction) - set(self._cards)
        return {card: 1 / len(cards) for card in cards}

    def get_active_player(self) -> int:
        if len(self._cards) < 2:
            return common.CHANCE_PLAYER

        if not self._history:
            return 0

        return self._get_other_player(self._history[-1].player)

    def get_inactive_player(self) -> int:
        return self._get_other_player(self.get_active_player())

    def apply_action(self, action: base_game.Action) -> None:
        if self.get_active_player() == common.CHANCE_PLAYER:
            self._cards.append(ChanceAction(action))
        else:
            self._history.append(PlayerAction(self.get_active_player(), Action(action)))

    def child(self, action: base_game.Action) -> KuhnPoker:
        new_game = KuhnPoker(copy.deepcopy(self._cards), copy.deepcopy(self._history))
        new_game.apply_action(action)

        return new_game
