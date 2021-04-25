from typing import List
import copy
from lib.grid import Grid
from lib.update_schemes import UpdateScheme


def simulate(grid: Grid, update_scheme: UpdateScheme, n_steps: int) -> List[Grid]:
    states: List[Grid] = [copy.deepcopy(grid)]
    for i in range(n_steps):
        update_scheme.update(grid)
        states.append(copy.deepcopy(grid))
    return states
