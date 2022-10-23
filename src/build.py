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
        
    def buildRays(self):
        # building the orthonomal base
        w: tuple = op.normalize(op.extractVector(*self.CAM_EYE, *self.CAM_LOOK_AT))
        u: tuple = op.normalize(op.crossProduct(*self.UP_VECTOR, *w))
        v: tuple = op.crossProduct(*w, *u) # não é necessário normalizar

        # calculanting the screen center
        screen_center = op.extractVector(self.CAM_EYE, op.escalarProd(self.DISTANCE, self.w)) # C = E - d W

        # calculating Q00
        n = 0.5*self.PIXEL_SIZE*self.HEIGHT
        m = 0.5*self.PIXEL_SIZE*self.WIDTH
        xc, yc, zc = screen_center
        xh, yh, zh = op.escalarProd(n-0.5*self.PIXEL_SIZE, v)
        xw, yw, zw = op.escalarProd(m-0.5*self.PIXEL_SIZE, u)
        x0, y0, z0 = (xc+xh, yc+yh, zc+zh)

        pixel_center_0 = (x0-xw, y0-yw, z0-zw) # Q00 = C + 1/2*s(n-1)*v - 1/2*s(m-1)*u

        # computing the rays direction
        for i in range(self.HEIGHT):
            for j in range(self.WIDTH):
                ...

