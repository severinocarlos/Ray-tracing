import numpy as np
from math import hypot, inf
from modules.ray import Ray
from modules.image import Image

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
        self.objs: list = scene_dict['object_list']
        
    def buildRays(self) -> Image:
        screen = Image(self.HEIGHT, self.WIDTH, self.BACKGROUND_COLOR) # creating a screen

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
        pixel_center_00 = screen_center + self.PIXEL_SIZE * (((self.HEIGHT - 1)/2) * v - ((self.WIDTH - 1)/2) * u)
        
        # computing the rays direction
        for i in range(self.HEIGHT):
            for j in range(self.WIDTH):
                current_position = pixel_center_00 + self.PIXEL_SIZE * (j * u - i * v)
                ray_direction = current_position - cam_eye  # alter
                ray_direction = normalize(ray_direction, norm(*ray_direction))
                ray = Ray(ray_direction, cam_eye)
                
                # setting the pixel color in the screen
                screen.set_pixel_color(i, j, self.cast(ray))
                
        
        return screen

    def cast(self, ray: Ray) -> list:
        cp = self.BACKGROUND_COLOR

        t, intersection, object = self.find_intersection(ray)
        # if not intersection:
        #     return self.BACKGROUND_COLOR
        # else:
        #     return object.color
        if not intersection:
            P = np.array(ray.origin + (t * ray.direction)) # intersection point
            v = -ray.direction # olhando para o observador
            n = object.normal(P)
            cp = self.shade(object, P, v, n)
    
    def find_intersection(self, ray: Ray, isIntersection = False, distance = inf) -> float | int:
        
        # checking the intersections for each object
        for object in self.objs:
            inter = object.intersect(ray)
            if inter <= distance:
                distance = inter
                current_object = object
            isIntersection = True if distance != inf else False

        return (distance, isIntersection, current_object)
    
    def shade(self, _object, _P, _v, _n):
        cp = np.multiply(_object.ka * _object.color, self.ambient_light)


        norm = lambda x, y, z : hypot(x,y,z)
        normalize = lambda a, b: a / b

        for C, L  in self.LIGHTS:
            l = np.array(L - _P)
            l = normalize(l, norm(*l))
            r = self.reflect(l, _n)

            light_point =  _P + 0.00001 * l
            ray = Ray(light_point, l)

            t, intersection, object = self.find_intersection(ray)

            if not intersection or np.dot(l, L - light_point) < t:
                if np.dot(_n, l) > 0:
                    cp += np.multiply(_object.kd * object.color, C * np.dot(_n, l))
                if np.dot(_v, r) > 0:
                    cp += _object.ks * (np.dot(_v, r) ** _object.exp) * C
        
        return cp

            
    def reflect(self, _l, _n):
        return 2((_n * _l) * (_n - _l))

