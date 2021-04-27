from typing import List
import copy
from lib.grid import Grid
from lib.update_schemes import UpdateScheme


def simulate(grid: Grid, update_scheme: UpdateScheme, n_steps: int, report_every: int = None,avoidOverlapping: bool = False) -> List[Grid]:
    states: List[Grid] = [copy.deepcopy(grid)]
    for i in range(n_steps):
        update_scheme.update(grid,avoidOverlapping)
        states.append(copy.deepcopy(grid))
        if report_every and i % report_every == 0:
            print("Simulated step {}".format(i))
    return states
