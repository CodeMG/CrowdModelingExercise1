from lib.grid import Grid
from lib.grid import CellType
import numpy as np

class Euclidean:
    def __init__(self,grid: Grid):
        self.grid = grid

    #Calculates the square root of start² + end² (For the euclidean distance)
    def euclidean_distance(self,start: (int,int),end: (int,int)) -> float:
        tmp = (start[0] - end[0])*(start[0] - end[0]) + (start[1] - end[1])*(start[1] - end[1])
        return np.sqrt(tmp)
    
    def euclidean_step(self) -> None:
        target = self.grid.get_target()
        pedestrians = self.grid.get_pedestrians()
        
        #For all the pedestrians, check if and neighboring cell is the target, if not then move to neighbouring cell closest to target
        for p in pedestrians:
            done = False
            closest_cell  = (0,0)
            closest_distance = self.euclidean_distance(closest_cell,tuple(target))
            
            #These for-loops are for checking all the neighboring cells
            for i in range(-1,2):
                for j in range(-1,2):
                    #Checking to make sure no out of bounds errors happen
                    if (p[0]+i) >= 0 and (p[0]+i) < self.grid.rows and (p[1]+j) >= 0 and (p[1]+j) < self.grid.columns:
                        #
                        if self.grid.grid[p[0]+i,p[1]+j] == CellType.TARGET:
                            done = True
                            break
                        elif self.grid.grid[p[0]+i,p[1]+j] == CellType.EMPTY:
                            current_distance = self.euclidean_distance((p[0]+i,p[1]+j),tuple(target))
                            if current_distance < closest_distance:
                                closest_cell = (p[0]+i,p[1]+j)
                                closest_distance = current_distance
                if done:
                    break
            if not done:
                self.grid.grid[p] = CellType.EMPTY
                self.grid.grid[closest_cell] = CellType.PEDESTRIAN
            
