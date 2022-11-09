import numpy as np


class Ray:
    def __init__(self,  origin, direction) -> None:
        ''' Abstract class '''
        self.direction = np.array(direction)
        self.origin = np.array(origin)
