from enum import IntEnum
import numpy as np

from typing import Tuple, List, Dict, NewType

Coordinates = NewType('Coordinatess', Tuple[int, int])
Pedestrian = NewType('Pedestrian', Tuple[Coordinates, float])


class CellType(IntEnum):
    EMPTY = 0
    OBSTACLE = 2
    TARGET = 3


class Grid:
    def __init__(self, rows: int, columns: int, pedestrians: List[Pedestrian], obstacles: List[Coordinates], target: Coordinates):
        self.rows = rows
        self.columns = columns
        self.obstacles = obstacles
        self.target = target
        self.grid = np.full((rows, columns), CellType.EMPTY, dtype=CellType)
        self.pedestrians = {
            10+i: pedestrians[i] for i in range(len(pedestrians))
        }
        self.update_pedestrians(self.pedestrians)
        self._put_obstacles(obstacles)
        self._put_target(target)

    def update_pedestrians(self, pedestrians: Dict[int, Pedestrian]) -> None:
        # set the cells with current pedestrians to EMPTY
        self.grid[self.grid >= 10] = CellType.EMPTY

        for key in pedestrians.keys():
            self.grid[pedestrians[key][0]] = key

        self.pedestrians = pedestrians

    def _put_target(self, target: Tuple[int, int]) -> None:
        self.grid[target[0], target[1]] = CellType.TARGET

    def _put_obstacles(self, obstacles: List[Coordinates]) -> None:
        for ob in obstacles:
            self.grid[ob[0], ob[1]] = CellType.OBSTACLE
