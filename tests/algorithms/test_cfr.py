"""CFR Tests."""

import pytest

from dd_cfr.algorithms import cfr
from dd_cfr.games import kuhn_poker


# See optimal strategy in https://en.wikipedia.org/wiki/Kuhn_poker.
@pytest.mark.parametrize(
    "regret_matching_plus,sampling_strategy,iterations",
    [
        #       (False, cfr.SamplingStrategy.FULL_SAMPLING, 1000),
        #       (False, cfr.SamplingStrategy.EXTERNAL_SAMPLING, 50000),
        (False, cfr.SamplingStrategy.OUTCOME_SAMPLING, 100000),
        #       (True, cfr.SamplingStrategy.FULL_SAMPLING, 1000),
    ],
)
def test_nash_equilibirum(regret_matching_plus, sampling_strategy, iterations):
    delta = 0.05
    cfr_solver = cfr.CFRSolver(
        regret_matching_plus=regret_matching_plus, sampling_strategy=sampling_strategy
    )
    cfr_solver.solve(kuhn_poker.KuhnPoker, iterations)
    policy = cfr_solver.get_policy()

    assert (
        policy[kuhn_poker.ChanceAction.JACK.name][kuhn_poker.Action.BET] < 1 / 3 + delta
    )

    assert policy[kuhn_poker.ChanceAction.QUEEN.name][
        kuhn_poker.Action.CHECK
    ] == pytest.approx(1, abs=delta)

    assert policy[kuhn_poker.ChanceAction.QUEEN.name][
        kuhn_poker.Action.BET
    ] == pytest.approx(0, abs=delta)

    assert policy[kuhn_poker.ChanceAction.KING.name][kuhn_poker.Action.BET] / policy[
        kuhn_poker.ChanceAction.JACK.name
    ][kuhn_poker.Action.BET] == pytest.approx(3, abs=delta * 5)

    assert policy["JACK|CHECK"][kuhn_poker.Action.BET] == pytest.approx(
        1 / 3, abs=delta
    )

    assert policy["JACK|BET"][kuhn_poker.Action.FOLD] == pytest.approx(1, abs=delta)

    assert policy["QUEEN|CHECK"][kuhn_poker.Action.CHECK] == pytest.approx(1, abs=delta)

    assert policy["QUEEN|BET"][kuhn_poker.Action.CALL] == pytest.approx(
        1 / 3, abs=delta
    )

    assert policy["KING|CHECK"][kuhn_poker.Action.BET] == pytest.approx(1, abs=delta)

    assert policy["KING|BET"][kuhn_poker.Action.CALL] == pytest.approx(1, abs=delta)
