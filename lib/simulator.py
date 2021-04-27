from typing import List
import copy
from lib.grid import Grid
from lib.update_schemes import UpdateScheme


def simulate(grid: Grid, update_scheme: UpdateScheme, n_steps: int, report_every: int = None,avoid_overlapping: bool = False) -> List[Grid]:
    """  
    This function simulates the given grid for a set amount of steps and returns a list with all the steps stored as grids
    :param grid: The Grid object which is supposed to be simulated
    :param update_scheme: The algorithm which is supposed to be used to decide how the pedestrians are going to move
    :param n_steps: How many steps are going to be simulated
    :param report_every: This indicates after how many steps a message is going to be printed (Helpful if there are a lot of steps and one wants to make sure that the code is progressing)
    :param avoid_overlapping: If set to True, this will makes it so that the pedestrians don't walk onto the same cell
    :return: A List of Grids that store all the steps of the simulation
    """
    states: List[Grid] = [copy.deepcopy(grid)]
    for i in range(n_steps):
        update_scheme.update(grid,avoid_overlapping)
        states.append(copy.deepcopy(grid))
        if report_every and i % report_every == 0:
            print("Simulated step {}".format(i))
    return states
