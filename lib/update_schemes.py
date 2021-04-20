from abc import ABC, abstractmethod
import numpy as np
import copy

from lib.grid import Grid, Coordinates


class UpdateScheme(ABC):

    @abstractmethod
    def get_costs(self, grid: Grid) -> np.ndarray:
        pass

    def update(self, grid: Grid) -> None:
        costs = self.get_costs(grid)

        # move the pedestrians
        moved_pedestrians = [self.move_pedestrian(
            p, costs) for p in grid.get_pedestrians()]

        # update the pedestrians
        grid.update_pedestrians(moved_pedestrians)

    def move_pedestrian(self, p: Coordinates, costs: np.ndarray) -> Coordinates:
        # all the neighbours of this pedestrian and the costs of moving there
        options = [p, (p[0] - 1, p[1]), (p[0] + 1, p[1]),
                   (p[0], p[1] - 1), (p[0], p[1] + 1)]
        options_with_cost = [
            (option, costs[option]) for option in options
            if 0 <= option[0] <= costs.shape[0]-1 and 0 <= option[1] <= costs.shape[1]-1
        ]
        return min(options_with_cost, key=lambda pair: pair[1])[0]


class RandomUpdateScheme(UpdateScheme):
    def get_costs(self, grid: Grid) -> np.ndarray:
        return np.random.rand(grid.rows, grid.columns)
