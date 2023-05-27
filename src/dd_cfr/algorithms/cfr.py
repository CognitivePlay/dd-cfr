"""Vanilla CFR implementation.

See https://poker.cs.ualberta.ca/publications/NIPS07-cfr.pdf."""

import collections
from typing import Dict, List, Mapping, Sequence, Type

from dd_cfr import common
from dd_cfr.games import base_game


class CFR:
    """CFR class."""

    def __init__(self) -> None:
        """
        Initialize CFR class.
        """

        # state, action to regret, to compute current policy.
        self.cummulative_regrets: Dict[
            str, Dict[base_game.Action, float]
        ] = collections.defaultdict(lambda: collections.defaultdict(float))
        # state, action to action probabilities, to compute averge policy.
        self.cummulative_policies: Dict[
            str, Dict[base_game.Action, float]
        ] = collections.defaultdict(lambda: collections.defaultdict(float))

    def _get_average(
        self,
        policy: Mapping[base_game.Action, float],
        possible_actions: Sequence[base_game.Action],
    ) -> Mapping[base_game.Action, float]:
        policy = {a: p for a, p in policy.items() if p >= 0 and a in possible_actions}
        sum_policy = sum(policy.values())

        if not sum_policy:
            return {action: 1 / len(possible_actions) for action in possible_actions}

        return {
            action: policy[action] / sum_policy if action in policy else 0
            for action in possible_actions
        }

    def print_policy(self) -> None:
        def _format_percentage(num: float) -> str:
            return f"{num:.1%}"

        for state, policy in sorted(self.cummulative_policies.items()):
            sum_policy = sum(policy.values())
            formatted_actions = ", ".join(
                f"{action.name}: {_format_percentage(s / sum_policy)}"
                for action, s in policy.items()
            )
            print(f"{state} - {formatted_actions}")

    def get_current_policy(
        self, state: str, legal_actions: Sequence[base_game.Action]
    ) -> Mapping[base_game.Action, float]:
        return self._get_average(self.cummulative_regrets[state], legal_actions)

    def get_average_policy(self, state: str) -> Mapping[base_game.Action, float]:
        return self._get_average(
            self.cummulative_policies[state],
            list(self.cummulative_policies[state].keys()),
        )

    def update(
        self,
        state: str,
        action: base_game.Action,
        regret: float,
        policy: float,
        reach_prob: float,
        regret_matching_plus: bool,
    ) -> None:
        self.cummulative_regrets[state][action] += regret * reach_prob
        if regret_matching_plus:
            self.cummulative_regrets[state][action] = max(
                self.cummulative_regrets[state][action], 0
            )

        self.cummulative_policies[state][action] += policy * reach_prob


class CFRSolver:
    """CFR Solver, traverses the provided game to compute a nash equilibrium."""

    def __init__(self, regret_matching_plus: bool = False) -> None:
        """
        Initialize CFRSolver class.

        :param regret_matching_plus: Whether to use regret matching plus, defaults to
            False.
        """
        self._cfr = CFR()
        self._regret_matching_plus = regret_matching_plus

    def _traverse(self, game: base_game.Game, reach_probs: List[float]) -> List[float]:
        """
        Recurisvely traverses the game tree.

        :param game: The game to traverse.
        :param reach_probs: The current reach probabilities.
        :return: The expected payoffs for both players.
        :raises ValueError: If different policy and legal_actions length encounetered.

        """
        if not game.is_terminal():
            if game.get_active_player() == common.CHANCE_PLAYER:
                policy = game.get_chance_probabilities()
            else:
                legal_actions = game.get_legal_actions()
                policy = self._cfr.get_current_policy(game.get_state(), legal_actions)
                if len(policy) != len(legal_actions):
                    raise ValueError(
                        "Length of policy and legal_actions must be identical got"
                        f" {len(policy)} and {len(legal_actions)}"
                    )

            rewards = {}
            for action, probability in policy.items():
                next_reach_probs = reach_probs[:]
                next_reach_probs[game.get_active_player()] *= probability
                rewards[action] = self._traverse(game.child(action), next_reach_probs)

            payoffs = [0.0, 0.0]

            for action in policy:
                for player_id in range(2):
                    payoffs[player_id] += rewards[action][player_id] * policy[action]

            if game.get_active_player() != common.CHANCE_PLAYER:
                for action in policy:
                    regret = (
                        rewards[action][game.get_active_player()]
                        - payoffs[game.get_active_player()]
                    )
                    self._cfr.update(
                        game.get_state(),
                        action,
                        regret,
                        policy[action],
                        reach_probs[game.get_inactive_player()],
                        self._regret_matching_plus,
                    )

            return payoffs

        else:
            return game.get_payoffs()

    def solve(self, game: Type[base_game.Game], iterations: int) -> None:
        """
        Solve a nash equilibrium for the provided game.

        :param game: The game to solve.
        :param iterations: Number of traversals.
        """
        for _ in range(iterations):
            self._traverse(game(), [1, 1, 1])

    def print_policy(self) -> None:
        """
        Prints the computed policy.
        """
        self._cfr.print_policy()
