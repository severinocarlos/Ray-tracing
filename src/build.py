import numpy
from modules import operations as op


class Build:
    def __init__(self, scene_dict) -> None:
        self.HEIGHT: int = scene_dict['v_res']
        self.WIDTH: int  = scene_dict['h_res']
        self.PIXEL_SIZE: float = scene_dict['square_side']
        self.DISTANCE: float = scene_dict['dist']
        self.CAM_EYE: list = scene_dict['eye']
        self.CAM_LOOK_AT: list = scene_dict['look_at']
        self.UP_VECTOR: list = scene_dict['up']
        self.BACKGROUND_COLOR: list = scene_dict['background_color']
        self.OBJECTS: list = scene_dict['objects']
        
    def rayDirection(self):
        # building the orthonomal base
        w: tuple = op.normalize(op.ExtractVector(*self.CAM_EYE, *self.CAM_LOOK_AT))
        u: tuple = op.normalize(op.crossProduct(*self.UP_VECTOR, *w))
        v: tuple = op.normalize(op.crossProduct(*w, *u))

        # calculanting the screen center
        screen_center = op.ExtractVector(self.CAM_EYE, op.EscalarProd(self.DISTANCE, self.w)) # C = E - d W
        
        # computing the rays direction
        for i in range(self.HEIGHT):
            for j in range(self.WIDTH):
                ...

