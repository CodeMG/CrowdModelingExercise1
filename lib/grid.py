from enum import Enum
import numpy as np

from typing import Tuple, List, NewType

Coordinate = NewType('Coordinate', Tuple[int, int])


class CellType(Enum):
    EMPTY = 0
    PEDESTRIAN = 1
    OBSTACLE = 2
    TARGET = 3


class Grid:
    def __init__(self, rows: int, columns: int, pedestrians: List[Coordinate], obstacles: List[Coordinate], target: Coordinate):
        self.rows = rows
        self.columns = columns
        self.obstacles = obstacles
        self.target = target
        self.grid = np.full((rows, columns), CellType.EMPTY, dtype=CellType)
        self._put_pedestrians(pedestrians)
        self._put_obstacles(obstacles)
        self._put_target(target)

    def _put_pedestrians(self, pedestrians: List[Coordinate]) -> None:
        for p in pedestrians:
            self.grid[p[0], p[1]] = CellType.PEDESTRIAN

    def _put_target(self, target: Tuple[int, int]) -> None:
        self.grid[target[0], target[1]] = CellType.TARGET

    def _put_obstacles(self, obstacles: List[Coordinate]) -> None:
        for ob in obstacles:
            self.grid[ob[0], ob[1]] = CellType.OBSTACLE

    def get_pedestrians(self) -> List[Coordinate]:
        return list(map(tuple, np.argwhere(self.grid == CellType.PEDESTRIAN)))
