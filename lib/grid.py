from enum import IntEnum
import numpy as np

from typing import Tuple, List, Dict, NewType

#The Coordinates type stores the positions of the cells
Coordinates = NewType('Coordinatess', Tuple[int, int])
#The Pedestrian type stores the information which a pedestrian has (position and speed)
Pedestrian = NewType('Pedestrian', Tuple[Coordinates, float])


class CellType(IntEnum):
    '''
    This is an enum containing the different states a cell in the grid can be
    '''
    EMPTY = 0
    OBSTACLE = 2
    TARGET = 3


class Grid:
    def __init__(self, rows: int, columns: int, pedestrians: List[Pedestrian], obstacles: List[Coordinates], target: Coordinates):
        """  
        :param rows: How many rows is the grid going to have
        :param columns: How many columns is the grid going to have
        :param pedestrians: A List filled with all the pedestrians
        :param obstacles: A List filled with the positions of all the obstacles
        :param target: The position of the target cell
        """
        self.rows = rows
        self.columns = columns
        self.obstacles = obstacles
        self.target = target
        self.grid = np.full((rows, columns), CellType.EMPTY, dtype=CellType) # An empty Grid
        self.pedestrians = {
            10+i: pedestrians[i] for i in range(len(pedestrians)) # The peedstrians all have a unique ID starting with 10
        }
        self.update_pedestrians(self.pedestrians)
        self._put_obstacles(obstacles)
        self._put_target(target)

    def update_pedestrians(self, pedestrians: Dict[int, Pedestrian]) -> None:
        """  
        This function positions the pedestrians on the grid
        :param pedestrians: A dictionary containing the IDs of the pedestrians and their corresponding data
        """
        # set the cells with current pedestrians to EMPTY
        self.grid[self.grid >= 10] = CellType.EMPTY

        for key in pedestrians.keys():
            self.grid[pedestrians[key][0]] = key

        self.pedestrians = pedestrians
        
    def update_pedestrian(self, pedestrian: Coordinates, key: int) -> None:
        """  
        This function positions only one pedestrian on the grid (needed to make sure that (if enabled) pedestrians can't overlap)
        :param pedestrian: The position of the pedestrian
        :param key: The ID of the pedestrian who is being updated
        """
        # set the cells with current pedestrians to EMPTY
        self.grid[self.grid is key] = CellType.EMPTY
        self.grid[self.pedestrians[key][0]] = key
        self.pedestrians[key] = pedestrian
    
    def _put_target(self, target: Tuple[int, int]) -> None:
        """  
        This function places a target on the grid
        :param target: The Position where a target is supposed to be placed
        """
        self.grid[target[0], target[1]] = CellType.TARGET

    def _put_obstacles(self, obstacles: List[Coordinates]) -> None:
        """  
        This function places the obstacles on the grid
        :param obstacles: A list with the positions where the obstacles are going to be placed
        """
        for ob in obstacles:
            self.grid[ob[0], ob[1]] = CellType.OBSTACLE
