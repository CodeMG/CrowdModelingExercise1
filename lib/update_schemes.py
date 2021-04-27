from abc import ABC, abstractmethod
import numpy as np
from typing import List

from lib.grid import Grid, Coordinates, Pedestrian, CellType
import random


class UpdateScheme(ABC):
    # This class is the parent class for all update schemes
    @abstractmethod
    def get_costs(self, grid: Grid) -> np.ndarray:
        """ 
        This is the abstract class which is supposed to be implemented by all the classes inheriting from this class
        :param grid: The grid for which the cost is supposed to be calculated
        :return: A array containing the costs of all the cells
        """ 
        pass

    def update(self, grid: Grid, avoid_overlapping: bool) -> None:
        """ 
        This function calles another function to determine the costs of the cells and then decides to which cells the pedestrians are supposed to move
        :param grid: The grid for which the update step is going to be done
        :param avoid_overlapping: If set to true, then the pedestrians are not going to overlap (a lot slower)
        """ 
        
        if avoid_overlapping:
            for key in grid.pedestrians.keys():
                costs = self.get_costs(grid)
                grid.update_pedestrian(self.move_pedestrian(grid.pedestrians[key], costs),key)
        else:
            costs = self.get_costs(grid)

            # move the pedestrians
            moved_pedestrians = {key: self.move_pedestrian(
                grid.pedestrians[key], costs) for key in grid.pedestrians.keys()}

            # update the pedestrians
            grid.update_pedestrians(moved_pedestrians)

    def move_pedestrian(self, p: Pedestrian, costs: np.ndarray) -> Pedestrian:
        """ 
        This function moves the pedestrian to the cell with the lowest cost
        Randomness was added to this function to simulate speed
        :param p: Then pedestrian who is supposed to be moves
        :param costs: The array containing the cost of all the cells
        :return: The Pedestrian with its updated position
        """ 
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
        """ 
        This function calculates the euclidean distance between two coordinates
        :param c1: The start coordinate
        :param c2: The end coordinate
        :return: The distance between the two coordinates
        """ 
        return np.sqrt((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2)

    @classmethod
    def get_indices(cls, rows: int, columns: int) -> List[Coordinates]:
        """ 
        This is a helper function. It returns a List of coordinates for a grid with the given size
        :param rows: How many rows the grid has
        :param columns: How many columns the grid has
        :return: A List with coordinates corresponding to all the cells. Useful for iterating over all the cells
        """ 
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
        """ 
        This is a helper function. It returns a List of coordinates for all the neighbours of a given cell
        :param c: The cell for which the neighbours need to be found
        :param rows: How many rows the grid has
        :param columns: How many columns the grid has
        :param diagonal: Are diagonal cells to be considered when determining the neighbours
        :return: A List with coordinates corresponding to all the neighbouring cells
        """ 
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
    # This update scheme set the cost of the cells randomly
    def get_costs(self, grid: Grid) -> np.ndarray:
        """ 
        This function returns an array with all the costs of the cells
        :param grid: The grid for which the costs ar esupposed to be determined
        :return: An array containing the costs of all the cells
        """ 
        return np.random.rand(grid.rows, grid.columns)


class EuclideanUpdateScheme(UpdateScheme):
    # This update scheme uses the basic euclidean distance between the cell and the target as the cost of the cells
    def get_costs(self, grid: Grid) -> np.ndarray:
        """ 
        This function returns an array with all the costs of the cells
        :param grid: The grid for which the costs ar esupposed to be determined
        :return: An array containing the costs of all the cells
        """ 
        # initialize with zeros
        costs = np.zeros((grid.rows, grid.columns))

        #
        indices = UpdateScheme.get_indices(grid.rows, grid.columns)
        for c in indices:
            costs[c] = self.d(c, grid.target)
        for key in grid.pedestrians.keys():
            costs[grid.pedestrians[key][0]] = 1000

        return costs


class DijkstraUpdateScheme(UpdateScheme):
    # This update scheme implements dijkstras algorithm to determine the cost of the cells
    def get_costs(self, grid: Grid):
        """ 
        This function returns an array with all the costs of the cells
        :param grid: The grid for which the costs ar esupposed to be determined
        :return: An array containing the costs of all the cells
        """ 
        # initialize with infinity
        costs = np.ones((grid.rows, grid.columns)) * np.inf

        def recursively_populate_neighbours(c: Coordinates, d: int):
            costs[c] = d
            for nc in DijkstraUpdateScheme.get_neighbours(c, grid.rows, grid.columns):
                if nc not in grid.obstacles and costs[nc] > d+1:
                    recursively_populate_neighbours(nc, d+1)

        recursively_populate_neighbours(grid.target, 0)
        for key in grid.pedestrians.keys():
            costs[grid.pedestrians[key][0]] = 1000
        return costs


class EuclideanInteractiveUpdateScheme(UpdateScheme):
    # This update scheme is the basic euclidean update scheme with the c_r function to make the pedestrians avoid other pedestrians
    def __init__(self, r_max: float):
        self.r_max = r_max

    def get_costs(self, grid: Grid) -> np.ndarray:
        """ 
        This function returns an array with all the costs of the cells
        :param grid: The grid for which the costs ar esupposed to be determined
        :return: An array containing the costs of all the cells
        """ 
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
        for key in grid.pedestrians.keys():
            costs[grid.pedestrians[key][0]] = 1000

        return costs


class EuclideanObstacleAvoidingUpdateScheme(UpdateScheme):
    # This update scheme is a basic euclidean update scheme with the c_r function to make the pedestrians avoid other pedestrians
    # And it also implements a very basic obstacle avoidance system
    def __init__(self, r_max: float):
        self.r_max = r_max

    def get_costs(self, grid: Grid) -> np.ndarray:
        """ 
        This function returns an array with all the costs of the cells
        :param grid: The grid for which the costs ar esupposed to be determined
        :return: An array containing the costs of all the cells
        """ 
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
                        
        for key in grid.pedestrians.keys():
            costs[grid.pedestrians[key][0]] = 1000

        return costs
