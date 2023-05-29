"""
Vanilla CFR implementation.

See https://poker.cs.ualberta.ca/publications/NIPS07-cfr.pdf.
"""

import collections
from typing import Dict, List, Mapping, Sequence, Tuple, Type

from dd_cfr import common
from dd_cfr.games import base_game


class CFR:
    """CFR class."""

    def __init__(self) -> None:
        """Initialize CFR class."""
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

    def get_current_policy(
        self, state: str, legal_actions: Sequence[base_game.Action]
    ) -> Mapping[base_game.Action, float]:
        """Return the current policy for a given state based on previous regrets.

        :param state: The state to the get policy for.
        :param legal_actions: The legal actions to consider.
        :return: The current policy.
        """
        return self._get_average(self.cummulative_regrets[state], legal_actions)

    def get_average_policy(self, state: str) -> Mapping[base_game.Action, float]:
        """Return the average policy over all iterations for a given state.

        This average policy converges to a nash equilibirum in the limit.

        :param state: The state to get the policy for.
        :return: The average policy.
        """
        return self._get_average(
            self.cummulative_policies[state],
            list(self.cummulative_policies[state].keys()),
        )

    def get_policy(self) -> Dict[str, Dict[base_game.Action, float]]:
        """Return the average policy for all observed states.

        :return: The average policy for all observed states.
        """
        policy = {}
        for state in self.cummulative_policies.keys():
            policy[state] = self.get_average_policy(state)

        return policy

    def update(
        self,
        state: str,
        action: base_game.Action,
        regret: float,
        policy: float,
        reach_prob: float,
        regret_matching_plus: bool,
    ) -> None:
        """Update regrets for a given state/action pair.

        :param state: The state to update regrets for.
        :param action: The corresponding action to update regrets for.
        :param regret: The observed regret.
        :param policy: The probability for the chosen action.
        :param reach_prob: The reach probability of the given state, ignoring the
            currently active player.
        :param regret_matching_plus: Whether to use regret-matching+
            (https://arxiv.org/abs/1407.5042).
        """
        self.cummulative_regrets[state][action] += regret * reach_prob
        if regret_matching_plus:
            self.cummulative_regrets[state][action] = max(
                self.cummulative_regrets[state][action], 0
            )

        self.cummulative_policies[state][action] += policy * reach_prob


class CFRSolver:
    """CFR Solver, traverses the provided game to compute a nash equilibrium."""

    def __init__(self, regret_matching_plus: bool = False) -> None:
        """Initialize CFRSolver class.

        :param regret_matching_plus: Whether to use regret matching plus, defaults to
            False.
        """
        self._cfr = CFR()
        self._regret_matching_plus = regret_matching_plus

    def _traverse(
        self,
        game: base_game.Game,
        reach_probs: Tuple[float, float, float] = (1.0, 1.0, 1.0),
    ) -> List[float]:
        """Recurisvely traverse the game tree.

        :param game: The game to traverse.
        :param reach_probs: The current reach probabilities for player 1, player 2 and
            the chance player.
        :return: The expected payoffs for both players.
        """
        if not game.is_terminal():
            if game.get_active_player() == common.CHANCE_PLAYER:
                policy = game.get_chance_probabilities()
            else:
                legal_actions = game.get_legal_actions()
                policy = self._cfr.get_current_policy(game.get_state(), legal_actions)

            rewards = {}
            for action, probability in policy.items():
                next_reach_probs = list(reach_probs)
                next_reach_probs[game.get_active_player()] *= probability
                rewards[action] = self._traverse(
                    game.child(action), tuple(next_reach_probs)
                )

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
                        reach_probs[game.get_inactive_player()]
                        * reach_probs[common.CHANCE_PLAYER],
                        self._regret_matching_plus,
                    )

            return payoffs

        else:
            return game.get_payoffs()

    def solve(self, game: Type[base_game.Game], iterations: int) -> None:
        """Solve a nash equilibrium for the provided game.

        :param game: The game to solve.
        :param iterations: Number of traversals.
        """
        for _ in range(iterations):
            self._traverse(game())

    def get_policy(self) -> Dict[str, Dict[base_game.Action, float]]:
        """Return the computed policy.

        :return: The computed policy for all states.
        """
        return self._cfr.get_policy()

    def print_policy(self) -> None:  # pragma: no cover
        """Print the computed policy."""

        def _format_percentage(num: float) -> str:
            return f"{num:.1%}"

        for state, policy in sorted(self.get_policy().items()):
            formatted_actions = ", ".join(
                f"{action.name}: {_format_percentage(p)}"
                for action, p in policy.items()
            )
            print(f"{state} - {formatted_actions}")
