from sqlite3 import enable_shared_cache
import numpy
from modules.operations import *

class Build:
    def __init__(self, scene_dict: dict) -> None:
        self.HEIGHT: int = scene_dict['v_res']
        self.WIDTH: int  = scene_dict['h_res']
        self.PIXEL_SIZE: float = scene_dict['square_side']
        self.DISTANCE: float = scene_dict['dist']
        self.CAM_EYE: list = scene_dict['eye']
        self.CAM_LOOK_AT: list = scene_dict['look_at']
        self.UP_VECTOR: list = scene_dict['up']
        self.BACKGROUND_COLOR: list = scene_dict['background_color']
        self.OBJECTS: list = scene_dict['objects']
        
    def buildRays(self):
        # building the orthonomal base
        w: tuple = normalize(sub(*self.CAM_EYE, *self.CAM_LOOK_AT))
        u: tuple = normalize(crossProduct(*self.UP_VECTOR, *w))
        v: tuple = crossProduct(*w, *u) # não é necessário normalizar

        # calculanting the screen center
        screen_center = sub(*self.CAM_EYE, *escalarProd(self.DISTANCE, w)) # C = E - d W

        # calculating Q00 -> C + 1/2*s(n-1)*v - 1/2*s(m-1)*u

        aux_sub = sub(*escalarProd((1/2*self.PIXEL_SIZE*(self.HEIGHT-1)), v), *escalarProd((1/2*self.PIXEL_SIZE*(self.WIDTH-1)), u))
        
        pixel_center_00 = sum(*screen_center, *aux_sub)

        # computing the rays direction
        for i in range(self.HEIGHT):
            for j in range(self.WIDTH):
                aux_sum = escalarProd(self.PIXEL_SIZE, sub(*escalarProd(j, u), *escalarProd(i, v)))
                current_position = sum(*pixel_center_00, *aux_sum)
                ray_direction = normalize(sub(*self.CAM_EYE, *current_position))
                # chamar ray_tracing()

    # def ray_tracing(self):