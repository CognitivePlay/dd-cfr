"""CFR Tests."""

from dd_cfr.algorithms import cfr
from dd_cfr.games import kuhn_poker


def test_cfr():
    cfr_solver = cfr.CFRSolver()
    cfr_solver.solve(kuhn_poker.KuhnPoker, 100)

    cfr_solver.print_policy()
