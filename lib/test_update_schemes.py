import unittest
import numpy as np
from lib.grid import Grid
from lib.update_schemes import EuclideanUpdateScheme


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
                (1, 0),
                (0, 1)
            ]
        )

    def test_euclidean_update_scheme(self):
        update_scheme = EuclideanUpdateScheme()
        costs = update_scheme.get_costs(self.grid)
        self.assertEqual(costs.shape, self.grid.grid.shape)
        self.assertEqual(costs[3, 5], 0)  # distance at target is 0
        self.assertEqual(costs[1, 5], 2)
