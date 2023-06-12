"""CFR Tests."""

import unittest

from dd_cfr.algorithms import cfr
from dd_cfr.games import kuhn_poker


class TestCfr(unittest.TestCase):
    """CFR Tests."""

    def test_nash_equilibirum(self):
        """See optimal strategy in https://en.wikipedia.org/wiki/Kuhn_poker."""

        delta = 0.05

        for regret_matching_plus in [False, True]:
            with self.subTest(regret_matching_plus=regret_matching_plus):
                cfr_solver = cfr.CFRSolver(regret_matching_plus=regret_matching_plus)
                cfr_solver.solve(kuhn_poker.KuhnPoker, 1000)
                policy = cfr_solver.get_policy()

                self.assertLessEqual(
                    policy[kuhn_poker.ChanceAction.JACK.name][kuhn_poker.Action.BET],
                    1 / 3 + delta,
                )

                self.assertAlmostEqual(
                    policy[kuhn_poker.ChanceAction.QUEEN.name][kuhn_poker.Action.CHECK],
                    1,
                    delta=delta,
                )

                self.assertAlmostEqual(
                    policy[kuhn_poker.ChanceAction.QUEEN.name][kuhn_poker.Action.BET],
                    0,
                    delta=delta,
                )

                self.assertAlmostEqual(
                    policy[kuhn_poker.ChanceAction.KING.name][kuhn_poker.Action.BET]
                    / policy[kuhn_poker.ChanceAction.JACK.name][kuhn_poker.Action.BET],
                    3,
                    delta=delta * 5,
                )

                self.assertAlmostEqual(
                    policy["JACK|CHECK"][kuhn_poker.Action.BET],
                    1 / 3,
                    delta=delta,
                )

                self.assertAlmostEqual(
                    policy["JACK|BET"][kuhn_poker.Action.FOLD],
                    1,
                    delta=delta,
                )

                self.assertAlmostEqual(
                    policy["QUEEN|CHECK"][kuhn_poker.Action.CHECK],
                    1,
                    delta=delta,
                )

                self.assertAlmostEqual(
                    policy["QUEEN|BET"][kuhn_poker.Action.CALL],
                    1 / 3,
                    delta=delta,
                )

                self.assertAlmostEqual(
                    policy["KING|CHECK"][kuhn_poker.Action.BET],
                    1,
                    delta=delta,
                )

                self.assertAlmostEqual(
                    policy["KING|BET"][kuhn_poker.Action.CALL],
                    1,
                    delta=delta,
                )
