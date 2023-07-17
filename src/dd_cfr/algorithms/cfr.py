"""Vanilla CFR implementation.

See https://poker.cs.ualberta.ca/publications/NIPS07-cfr.pdf.
"""

import collections
import enum
import random
from typing import Optional, Sequence, Type

from dd_cfr import common
from dd_cfr.games import base_game


class SamplingStrategy(enum.Enum):
    """The sampling strategy  for CFR traversals."""

    # Traverse all paths.
    FULL_SAMPLING = 0
    # Outcome sampling: only traverse a single path each iteration.
    OUTCOME_SAMPLING = 1
    # External sampling: traverse all player actions; sample chance and other players.
    EXTERNAL_SAMPLING = 2


class CFR:
    """CFR class."""

    def __init__(self) -> None:
        """Initialize CFR class."""
        # Maps state and action to regret. Used to compute the current policy.
        self.cumulative_regrets: dict[
            str, dict[base_game.Action, float]
        ] = collections.defaultdict(lambda: collections.defaultdict(float))
        # Maps state and action to regret. Used to compute the average policy.
        self.cumulative_policies: dict[
            str, dict[base_game.Action, float]
        ] = collections.defaultdict(lambda: collections.defaultdict(float))

    def _get_average(
        self,
        policy: dict[base_game.Action, float],
        possible_actions: Sequence[base_game.Action],
    ) -> dict[base_game.Action, float]:
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
    ) -> dict[base_game.Action, float]:
        """Return the current policy for a given state based on previous regrets.

        :param state: The state to the get policy for.
        :param legal_actions: The legal actions to consider.
        :return: The current policy.
        """
        return self._get_average(self.cumulative_regrets[state], legal_actions)

    def get_average_policy(self, state: str) -> dict[base_game.Action, float]:
        """Return the average policy over all iterations for a given state.

        This average policy converges to a nash equilibirum in the limit.

        :param state: The state to get the policy for.
        :return: The average policy.
        """
        return self._get_average(
            self.cumulative_policies[state],
            list(self.cumulative_policies[state].keys()),
        )

    def get_policy(self) -> dict[str, dict[base_game.Action, float]]:
        """Return the average policy for all observed states.

        :return: The average policy for all observed states.
        """
        policy = {}
        for state in self.cumulative_policies.keys():
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
        self.cumulative_regrets[state][action] += regret * reach_prob
        if regret_matching_plus:
            self.cumulative_regrets[state][action] = max(
                self.cumulative_regrets[state][action], 0
            )

        self.cumulative_policies[state][action] += policy * reach_prob


class CFRSolver:
    """CFR Solver, traverses the provided game to compute a nash equilibrium."""

    def __init__(
        self,
        sampling_strategy: SamplingStrategy = SamplingStrategy.FULL_SAMPLING,
        regret_matching_plus: bool = False,
        rng: Optional[random.Random] = None,
        epsilon: float = 0.05,
    ) -> None:
        """Initialize CFRSolver class.

        :param sampling_strategy: Which sampling strategy to use for traversals,
            defaults to full sampling.
        :param regret_matching_plus: Whether to use Whether to use regret-matching+
            (https://arxiv.org/abs/1407.5042), defaults to False.
        :param rng: The random number generator to use for sampling.
        :param epsilon: Epsilon to use for external and outcome sampling, i.e. the
            minimum the sampling probability to use for each action.
        """
        self._cfr = CFR()
        self._sampling_strategy = sampling_strategy
        self._regret_matching_plus = regret_matching_plus
        self._rng = rng or random.Random()
        self._epsilon = epsilon

    def _select_actions(
        self,
        policy: dict[base_game.Action, float],
        is_active_player: bool,
    ) -> dict[base_game.Action, tuple[float, float]]:
        """Select actions to traverse and corresponding sampling probabilities.

        :param policy: The policy to select actions from.
        :param is_active_player: Whether the traversal player is the active player.
            Relevant to decide on the sampling strategy for external sampling.
        :raises ValueError: For unsupported combinations of sampling strategy and
            is_active_player.
        :return: Map from chosen actions to policy and sampling probability.
        """

        if self._sampling_strategy == SamplingStrategy.FULL_SAMPLING or (
            self._sampling_strategy == SamplingStrategy.EXTERNAL_SAMPLING
            and is_active_player
        ):
            return {action: (prob, 1) for action, prob in policy.items()}
        elif self._sampling_strategy == SamplingStrategy.OUTCOME_SAMPLING or (
            self._sampling_strategy == SamplingStrategy.EXTERNAL_SAMPLING
            and not is_active_player
        ):
            weights = {action: max(p, self._epsilon) for action, p in policy.items()}
            weights_sum = sum(weights.values())
            sampling_probabilities = {
                action: w / weights_sum for action, w in weights.items()
            }
            sampled_action = self._rng.choices(
                population=list(policy.keys()),
                weights=list(sampling_probabilities.values()),
            )[0]
            return {
                sampled_action: (
                    policy[sampled_action],
                    sampling_probabilities[sampled_action],
                )
            }
        else:
            raise ValueError(
                f"Sampling strategy {self._sampling_strategy} not implemented for"
                f" is_active_player {is_active_player}"
            )

    def _traverse(
        self,
        game: base_game.Game,
        traversal_player: int,
        reach_probs: Sequence[float] = (1.0, 1.0, 1.0),
        sampling_prob: float = 1.0,
    ) -> Sequence[float]:
        """Recurisvely traverse the game tree.

        :param game: The game to traverse.
            done. Relevant for external sampling.
        :param traversal_player: The "active" traversal player, only relevant when using
            the sampling_strategy EXTERNAL_SAMPLING.
        :param reach_probs: The current reach probabilities for player 1, player 2, and
            the chance player.
        :param sampling_prob: The probability with which the current path has been
            sampled.
        :return: The expected payoffs for both players.
        """
        if not game.is_terminal():
            if game.get_active_player() == common.CHANCE_PLAYER:
                policy = game.get_chance_probabilities()
            else:
                legal_actions = game.get_legal_actions()
                policy = self._cfr.get_current_policy(game.get_state(), legal_actions)

            sampled_policy = self._select_actions(
                policy, game.get_active_player() == traversal_player
            )

            rewards = {}
            for action, (probability, current_sampling_prob) in sampled_policy.items():
                next_reach_probs = list(reach_probs)
                next_reach_probs[game.get_active_player()] *= probability
                rewards[action] = self._traverse(
                    game.child(action),
                    traversal_player,
                    reach_probs=next_reach_probs,
                    sampling_prob=sampling_prob * current_sampling_prob,
                )

            payoffs = [0.0, 0.0]

            for action, (probability, _) in sampled_policy.items():
                for player_id in range(2):
                    payoffs[player_id] += rewards[action][player_id] * probability

            if game.get_active_player() != common.CHANCE_PLAYER:
                for action, (probability, _) in sampled_policy.items():
                    regret = (
                        rewards[action][game.get_active_player()]
                        - payoffs[game.get_active_player()]
                    ) / sampling_prob
                    self._cfr.update(
                        game.get_state(),
                        action,
                        regret,
                        probability,
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
            random_traversal_player = self._rng.choice(range(2))
            self._traverse(game(), random_traversal_player)

    def get_policy(self) -> dict[str, dict[base_game.Action, float]]:
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
