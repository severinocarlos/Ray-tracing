import numpy as np
from math import hypot

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
        cam_eye = np.array(self.CAM_EYE)
        cam_look_at = np.array(self.CAM_LOOK_AT)
        up_vector = np.array(self.UP_VECTOR)
        distance = np.array(self.DISTANCE)
        
        norm = lambda x, y, z : hypot(x,y,z)
        normalize = lambda a, b: a / b

        # building the orthonomal base
        w = cam_eye - cam_look_at
        w = normalize(w, norm(*w))
        u = np.cross(up_vector, w)
        u = normalize(u, norm(*u))
        v = np.cross(w,u)

        # calculanting the screen center
        screen_center = cam_eye - distance * w
        
        # calculating Q[0][0] = C + (1/2 * s(n-1) * v) - (1/2 * s(m-1) * u)
        pixel_center_00 = screen_center + (1/2 * self.PIXEL_SIZE * (self.HEIGHT-1) * v) \
                                        - (1/2 * self.PIXEL_SIZE * (self.WIDTH-1) * u)
        
        # computing the rays direction
        for i in range(self.HEIGHT):
            for j in range(self.WIDTH):
                current_position = pixel_center_00 + self.PIXEL_SIZE * (j * u - i * v)
                ray_direction = cam_eye - current_position
                ray_direction = normalize(ray_direction, norm(*ray_direction))
                
    def ray_tracing(self):
        ...