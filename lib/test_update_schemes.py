import unittest
import numpy as np
from lib.grid import Grid
from lib.update_schemes import EuclideanUpdateScheme
from lib.update_schemes import DijkstraUpdateScheme

#This Class is just a class for testing the update schemes(Not used for anything else)
class UpdateSchemeTest(unittest.TestCase):
    def setUp(self):
        self.grid = Grid(
            rows=5,
            columns=6,
            target=(3, 5),
            obstacles=[
                (2, 3)
            ],
            pedestrians=[
                ((1, 0), 1),
                ((0, 1), 1)
            ]
        )

    def test_euclidean_update_scheme(self):
        update_scheme = EuclideanUpdateScheme()
        costs = update_scheme.get_costs(self.grid)
        self.assertEqual(costs.shape, self.grid.grid.shape)
        self.assertEqual(costs[3, 5], 0)  # distance at target is 0
        self.assertEqual(costs[1, 5], 2)

    def test_dijkstra_update_scheme(self):
        update_scheme = DijkstraUpdateScheme()
        costs = update_scheme.get_costs(self.grid)
        self.assertEqual(costs.shape, self.grid.grid.shape)
        self.assertEqual(costs[(2, 3)], np.inf)
        self.assertEqual(costs[(3, 5)], 0)
        self.assertEqual(costs[(2, 5)], 1)
