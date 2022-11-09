import numpy as np
from math import hypot, inf, sqrt
from modules.ray import Ray
from modules.image import Image
import random
from time import sleep

class Build:
    def __init__(self, scene_dict: dict) -> None:
        self.HEIGHT: int = scene_dict['v_res']
        self.WIDTH: int  = scene_dict['h_res']
        self.PIXEL_SIZE: float = scene_dict['square_side']
        self.DISTANCE: float = scene_dict['dist']
        self.CAM_EYE: list = scene_dict['eye']
        self.CAM_LOOK_AT: list = scene_dict['look_at']
        self.UP_VECTOR: list = scene_dict['up']
        self.BACKGROUND_COLOR: list = np.array(scene_dict['background_color'])/255
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
        
        num_samples = 25
        
        px_min = self.PIXEL_SIZE/ 50
        
        n = int(sqrt(num_samples))
        
        # computing the rays direction
        for i in range(self.HEIGHT):
            for j in range(self.WIDTH):
                sum_color = np.array([0.0,0.0,0.0])
                current_position = pixel_center_00 + self.PIXEL_SIZE * (j * u - i * v)
                
                for c in range(n):
                    current_position 
                    for r in range(n):
                        ray_direction = current_position - cam_eye  # alter
                        ray_direction = normalize(ray_direction, norm(*ray_direction))
                        
                        ray = Ray(ray_direction, cam_eye)
                        
                        # setting the pixel color in the screen
                        sum_color += self.rayCasting(ray)
                
                
                # current_position = pixel_center_00 + self.PIXEL_SIZE * (j * u - i * v)
                # ray_direction = current_position - cam_eye  # alter
                # ray_direction = normalize(ray_direction, norm(*ray_direction))
                
                # ray = Ray(ray_direction, cam_eye)
                
                # setting the pixel color in the screen
            #  self.rayCasting(ray)
                
            # sleep(1)
                print(sum_color)
                sleep(1)
                sum_color /= num_samples
                print(sum_color*255)
                screen.set_pixel_color(i, j, self.rayCasting(ray)*255)
                        
        
        return screen

    def rayCasting(self, ray: Ray) -> list:
        
        _, intersection, object = self.find_intersection(ray)
        # print(object)
        print(intersection)
        if not intersection:
            return self.BACKGROUND_COLOR
        else:
            return object.color
        
    
    def find_intersection(self, ray: Ray, isIntersection = False, distance = inf):
        

        # checking the intersections for each object
        for object in self.objs:
            inter = object.intersect(ray)
            if inter <= distance:
                distance = inter
                current_object = object
            isIntersection = True if distance != inf else False

        return (distance, isIntersection, current_object)
    
    def rand_float(self, px) -> float:
        return random.uniform(-px, px)
