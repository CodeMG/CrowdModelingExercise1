from abc import ABC, abstractmethod
import numpy as np
from typing import List

from lib.grid import Grid, Coordinates, CellType


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
                   (p[0], p[1] - 1), (p[0], p[1] + 1), (p[0] - 1, p[1] -1), (p[0] + 1, p[1] + 1), (p[0] - 1, p[1] +1), (p[0] + 1, p[1] - 1)]
        options_with_cost = [
            (option, costs[option]) for option in options
            if 0 <= option[0] <= costs.shape[0]-1 and 0 <= option[1] <= costs.shape[1]-1
        ]
        return min(options_with_cost, key=lambda pair: pair[1])[0]

    @classmethod
    def get_indices(cls, rows: int, columns: int) -> List[Coordinates]:
        indices = np.indices((rows, columns))
        return list(
            map(
                tuple,
                np.stack(
                    (indices[0].flatten(), indices[1].flatten()),
                    axis=-1
                )
            )
        )


class RandomUpdateScheme(UpdateScheme):
    def get_costs(self, grid: Grid) -> np.ndarray:
        return np.random.rand(grid.rows, grid.columns)

class EuclideanUpdateScheme(UpdateScheme):
    
    def d(self, c1: Coordinates, c2: Coordinates):
        return np.sqrt((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2)

    def get_costs(self, grid: Grid) -> np.ndarray:

        # initialize with zeros
        costs = np.zeros((grid.rows, grid.columns))

        #
        indices = UpdateScheme.get_indices(grid.rows, grid.columns)
        for c in indices:
            costs[c] = self.d(c, grid.target)

        return costs


class EuclideanInteractiveUpdateScheme(UpdateScheme):
    
    def __init__(self,r_max: float):
        self.r_max = r_max

    def d(self, c1: Coordinates, c2: Coordinates):
        return np.sqrt((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2)

    def get_costs(self, grid: Grid) -> np.ndarray:

        # initialize with zeros
        costs = np.zeros((grid.rows, grid.columns))
        indices = UpdateScheme.get_indices(grid.rows, grid.columns)
        for c in indices:
            costs[c] = self.d(c, grid.target)
            for p in grid.get_pedestrians():
                r = self.d(c,p)
                if r < self.r_max:
                    avoidance = np.exp(1/(r**2 - self.r_max**2))
                    costs[c] += avoidance
        

        return costs
    
class EuclideanObstacleAvoidingUpdateScheme(UpdateScheme):
    
    def __init__(self,r_max: float):
        self.r_max = r_max

    def d(self, c1: Coordinates, c2: Coordinates):
        return np.sqrt((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2)

    def get_costs(self, grid: Grid) -> np.ndarray:
        # initialize with zeros
        costs = np.zeros((grid.rows, grid.columns))
        indices = UpdateScheme.get_indices(grid.rows, grid.columns)
        for c in indices:
            if grid.grid[c] == CellType.OBSTACLE:
                costs[c] = 1000
            else:
                costs[c] = self.d(c, grid.target)
                for p in grid.get_pedestrians():
                    r = self.d(c,p)
                    if r < self.r_max:
                        avoidance = np.exp(1/(r**2 - self.r_max**2))
                        costs[c] += avoidance
        

        return costs