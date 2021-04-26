from ipycanvas import Canvas, hold_canvas
import numpy as np
from lib.grid import Grid


class GridDrawer:

    def __init__(self, canvas: Canvas):
        self.canvas = canvas

    def draw(self, grid: Grid):
        cell_width = self.canvas.width / grid.columns
        cell_height = self.canvas.height / grid.rows
        self.canvas.clear()
        with hold_canvas(self.canvas):
            # draw all cells empty
            indices = np.indices((grid.rows, grid.columns))
            row_indices = indices[0].flatten()
            column_indices = indices[1].flatten()
            self.canvas.stroke_rects(
                x=column_indices*cell_width,
                y=row_indices*cell_height,
                width=cell_width,
                height=cell_height
            )

            # draw pedestrians
            pedestrians_coordinates = [p[0] for p in grid.pedestrians.values()]
            self.canvas.fill_style = 'red'
            self.canvas.fill_rects(
                x=[p[1] * cell_width for p in pedestrians_coordinates],
                y=[p[0] * cell_height for p in pedestrians_coordinates],
                width=cell_width - 1,
                height=cell_height - 1
            )

            # draw obstacles
            self.canvas.fill_style = 'black'
            self.canvas.fill_rects(
                x=[p[1] * cell_width for p in grid.obstacles],
                y=[p[0] * cell_height for p in grid.obstacles],
                width=cell_width - 1,
                height=cell_height - 1
            )

            # draw target
            self.canvas.fill_style = 'green'
            self.canvas.fill_rect(
                grid.target[1] * cell_width,
                grid.target[0] * cell_height,
                cell_width - 1,
                cell_height - 1
            )

            return self.canvas
