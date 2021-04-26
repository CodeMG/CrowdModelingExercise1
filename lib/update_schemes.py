from abc import ABC, abstractmethod
import numpy as np
from typing import List

from lib.grid import Grid, Coordinates, Pedestrian, CellType
import random


class UpdateScheme(ABC):

    @abstractmethod
    def get_costs(self, grid: Grid) -> np.ndarray:
        pass

    def update(self, grid: Grid) -> None:
        costs = self.get_costs(grid)

        # move the pedestrians
        moved_pedestrians = {key: self.move_pedestrian(
            grid.pedestrians[key], costs) for key in grid.pedestrians.keys()}

        # update the pedestrians
        grid.update_pedestrians(moved_pedestrians)

    def move_pedestrian(self, p: Pedestrian, costs: np.ndarray) -> Pedestrian:
        # all the neighbours of this pedestrian and the costs of moving there
        neighbours = UpdateScheme.get_neighbours(
            p[0], costs.shape[0], costs.shape[1], diagonal=True) + [p[0]]

        options_with_cost_and_d = [
            (option, costs[option], self.d(option, p[0])) for option in neighbours
        ]
        best_option_with_d = min(
            options_with_cost_and_d, key=lambda triple: triple[1])

        r = random.random()
        if best_option_with_d[2] == 0 or r <= p[1]/best_option_with_d[2]:
            return (best_option_with_d[0], p[1])
        else:
            return p

    def d(self, c1: Coordinates, c2: Coordinates):
        return np.sqrt((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2)

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

    @classmethod
    def get_neighbours(cls, c: Coordinates, rows: int, columns: int, diagonal: bool = False) -> List[Coordinates]:
        options = [
            (c[0] - 1, c[1]),
            (c[0] + 1, c[1]),
            (c[0], c[1] - 1),
            (c[0], c[1] + 1)
        ]
        if diagonal:
            options += [
                (c[0] - 1, c[1] - 1),
                (c[0] + 1, c[1] + 1),
                (c[0] - 1, c[1] + 1),
                (c[0] + 1, c[1] - 1)
            ]
        return [
            option for option in options
            if 0 <= option[0] < rows and 0 <= option[1] < columns
        ]


class RandomUpdateScheme(UpdateScheme):
    def get_costs(self, grid: Grid) -> np.ndarray:
        return np.random.rand(grid.rows, grid.columns)


class EuclideanUpdateScheme(UpdateScheme):

    def get_costs(self, grid: Grid) -> np.ndarray:

        # initialize with zeros
        costs = np.zeros((grid.rows, grid.columns))

        #
        indices = UpdateScheme.get_indices(grid.rows, grid.columns)
        for c in indices:
            costs[c] = self.d(c, grid.target)

        return costs


class DijkstraUpdateScheme(UpdateScheme):
    def get_costs(self, grid: Grid):

        # initialize with infinity
        costs = np.ones((grid.rows, grid.columns)) * np.inf

        def recursively_populate_neighbours(c: Coordinates, d: int):
            costs[c] = d
            for nc in DijkstraUpdateScheme.get_neighbours(c, grid.rows, grid.columns):
                if nc not in grid.obstacles and costs[nc] > d+1:
                    recursively_populate_neighbours(nc, d+1)

        recursively_populate_neighbours(grid.target, 0)
        return costs


class EuclideanInteractiveUpdateScheme(UpdateScheme):

    def __init__(self, r_max: float):
        self.r_max = r_max

    def get_costs(self, grid: Grid) -> np.ndarray:

        # initialize with zeros
        costs = np.zeros((grid.rows, grid.columns))
        indices = UpdateScheme.get_indices(grid.rows, grid.columns)
        for c in indices:
            costs[c] = self.d(c, grid.target)
            for p in [p[0] for p in grid.pedestrians.values()]:
                r = self.d(c, p)
                if r < self.r_max:
                    avoidance = np.exp(1/(r**2 - self.r_max**2))
                    costs[c] += avoidance

        return costs


class EuclideanObstacleAvoidingUpdateScheme(UpdateScheme):

    def __init__(self, r_max: float):
        self.r_max = r_max

    def get_costs(self, grid: Grid) -> np.ndarray:
        # initialize with zeros
        costs = np.zeros((grid.rows, grid.columns))
        indices = UpdateScheme.get_indices(grid.rows, grid.columns)
        for c in indices:
            if grid.grid[c] == CellType.OBSTACLE:
                costs[c] = 1000
            else:
                costs[c] = self.d(c, grid.target)
                for p in [p[0] for p in grid.pedestrians.values()]:
                    r = self.d(c, p)
                    if r < self.r_max:
                        avoidance = np.exp(1/(r**2 - self.r_max**2))
                        costs[c] += avoidance

        return costs
