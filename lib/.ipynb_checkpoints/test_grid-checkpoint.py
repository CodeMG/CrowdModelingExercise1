import unittest
import numpy as np
from lib.grid import Grid


class GridTest(unittest.TestCase):

    def setUp(self):
        self.pedestrians = [
            (0, 0),
            (1, 2)
        ]
        self.target = (4, 5)
        self.obstacles = [
            (2, 1),
            (2, 3)
        ]
        self.grid = Grid(
            rows=5,
            columns=6,
            pedestrians=self.pedestrians,
            obstacles=self.obstacles,
            target=self.target
        )

    def test_grid_creation(self):
        self.assertEqual(self.grid.rows, 5)
        self.assertEqual(self.grid.columns, 6)
        self.assertIsInstance(self.grid.grid, np.ndarray)
        self.assertEqual(self.grid.grid.shape, (5, 6))

    def test_get_pedestrians(self):
        coords = self.grid.get_pedestrians()
        self.assertTrue(all(c in coords for c in self.pedestrians))

    def test_get_target(self):
        self.assertEqual(self.grid.target, self.target)

    def test_get_obstacles(self):
        self.assertEqual(len(self.grid.obstacles), len(self.obstacles))
        self.assertTrue(
            all(self.grid.obstacles[i] == self.obstacles[i]
                for i in range(len(self.obstacles)))
        )
