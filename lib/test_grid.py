import unittest
import numpy as np
from lib.grid import Grid

#This Class is just a class for testing the grid(Not used for anything else)
class GridTest(unittest.TestCase):
    
    def setUp(self):
        
        self.pedestrians = [
            ((0, 0), 1),
            ((1, 2), 1)
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

    def test_pedestrians(self):
        pedestrians = self.grid.pedestrians
        self.assertIn(10, pedestrians)
        self.assertIn(11, pedestrians)
        self.assertEquals(pedestrians[10], ((0, 0), 1))

    def test_get_target(self):
        self.assertEqual(self.grid.target, self.target)

    def test_get_obstacles(self):
        self.assertEqual(len(self.grid.obstacles), len(self.obstacles))
        self.assertTrue(
            all(self.grid.obstacles[i] == self.obstacles[i]
                for i in range(len(self.obstacles)))
        )
