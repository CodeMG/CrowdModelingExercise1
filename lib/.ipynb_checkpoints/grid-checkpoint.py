from enum import Enum
import numpy as np

from typing import Tuple, List, NewType

Coordinates = NewType('Coordinatess', Tuple[int, int])


class CellType(Enum):
    EMPTY = 0
    PEDESTRIAN = 1
    OBSTACLE = 2
    TARGET = 3


class Grid:
    def __init__(self, rows: int, columns: int, pedestrians: List[Coordinates], obstacles: List[Coordinates], target: Coordinates):
        self.rows = rows
        self.columns = columns
        self.obstacles = obstacles
        self.target = target
        self.grid = np.full((rows, columns), CellType.EMPTY, dtype=CellType)
        self.update_pedestrians(pedestrians)
        self._put_obstacles(obstacles)
        self._put_target(target)

    def update_pedestrians(self, pedestrians: List[Coordinates]) -> None:
        # set the cells with current pedestrians to EMPTY
        self.grid[self.grid == CellType.PEDESTRIAN] = CellType.EMPTY

        for p in pedestrians:
            self.grid[p[0], p[1]] = CellType.PEDESTRIAN

    def _put_target(self, target: Tuple[int, int]) -> None:
        self.grid[target[0], target[1]] = CellType.TARGET

    def _put_obstacles(self, obstacles: List[Coordinates]) -> None:
        for ob in obstacles:
            self.grid[ob[0], ob[1]] = CellType.OBSTACLE

    def get_pedestrians(self) -> List[Coordinates]:
        return list(map(tuple, np.argwhere(self.grid == CellType.PEDESTRIAN)))
