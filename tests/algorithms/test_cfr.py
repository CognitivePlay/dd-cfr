"""CFR Tests."""

import unittest

from dd_cfr.algorithms import cfr
from dd_cfr.games import kuhn_poker


class TestCfr(unittest.TestCase):
    """CFR Tests."""

    def test_nash_equilibirum(self):
        """See optimal strategy in https://en.wikipedia.org/wiki/Kuhn_poker."""

        cfr_solver = cfr.CFRSolver()
        cfr_solver.solve(kuhn_poker.KuhnPoker, 2000)
        policy = cfr_solver.get_policy()

        self.assertLessEqual(
            policy[kuhn_poker.ChanceAction.JACK.name][kuhn_poker.Action.BET],
            1 / 3,
        )

        self.assertAlmostEqual(
            policy[kuhn_poker.ChanceAction.QUEEN.name][kuhn_poker.Action.CHECK],
            1,
            delta=0.02,
        )

        self.assertAlmostEqual(
            policy[kuhn_poker.ChanceAction.QUEEN.name][kuhn_poker.Action.BET],
            0,
            delta=0.02,
        )

        self.assertAlmostEqual(
            policy[kuhn_poker.ChanceAction.KING.name][kuhn_poker.Action.BET]
            / policy[kuhn_poker.ChanceAction.JACK.name][kuhn_poker.Action.BET],
            3,
            delta=0.2,
        )

        self.assertAlmostEqual(
            policy["JACK|CHECK"][kuhn_poker.Action.BET],
            1 / 3,
            delta=0.02,
        )

        self.assertAlmostEqual(
            policy["JACK|BET"][kuhn_poker.Action.FOLD],
            1,
            delta=0.02,
        )

        self.assertAlmostEqual(
            policy["QUEEN|CHECK"][kuhn_poker.Action.CHECK],
            1,
            delta=0.02,
        )

        self.assertAlmostEqual(
            policy["QUEEN|BET"][kuhn_poker.Action.CALL],
            1 / 3,
            delta=0.02,
        )

        self.assertAlmostEqual(
            policy["KING|CHECK"][kuhn_poker.Action.BET],
            1,
            delta=0.02,
        )

        self.assertAlmostEqual(
            policy["KING|BET"][kuhn_poker.Action.CALL],
            1,
            delta=0.02,
        )
