import numpy as np
from math import hypot, inf, sqrt
from modules.ray import Ray
from modules.image import Image
from modules.light import Light
from random import uniform
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
        self.lights: list = scene_dict['lights']
        self.ambient_light = np.array(scene_dict['ambient_light'])/255
        
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
                ray = Ray(origin=cam_eye, direction=ray_direction)
                
                # setting the pixel color in the screen
                color = np.array(self.cast(ray))
                color = color*255 / max(1, *color)
                screen.set_pixel_color(i, j, color)
            print(f'{i * j} - {self.HEIGHT * self.WIDTH}', end= '\r')     
        return screen

    def cast(self, ray: Ray) -> list:
        cp = self.BACKGROUND_COLOR
        t, intersection, object = self.find_intersection(ray)
        
        if intersection:
            P = np.array(ray.origin + (t * ray.direction)) # intersection point
            v = np.array([-i for i in ray.direction])
            normal_vector = object.normal(P)
            cp = self.shade(object, P, v, normal_vector)

        return cp
    
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

        num_samples = 25
        n = int(sqrt(num_samples))
        px = 40 / num_samples * 2
        
        for light in self.lights:
            
            light_center = light.position
            u = np.array(light.a2 - light.a4)
            v = np.array(light.a3 - light.a4)
            u = normalize(u, norm(*u))
            v = normalize(v, norm(*v))
            
            height = 200
            width = 200
            pixel_size = 40

            # pixel_center_00 = screen_center + self.PIXEL_SIZE * (((self.HEIGHT - 1)/2) * v - ((self.WIDTH - 1)/2) * u)
            pixel_center_00 =  light_center + pixel_size * (((height - 1)/2) * v - ((width - 1)/2) * u)
            
            for i in range(height):
                for j in range(width):
                    current_position = pixel_center_00 + pixel_size * (j * u - i * v)
                    # soft shadows ?
                    for c in range(n):
                        for r in range(n):
                            sub_pixel = current_position + pixel_size / 2 * (1 - 1 / n) * (v - u)
                            current_sub_pixel =  sub_pixel + pixel_size / 2 * ((r + self.rand_float(px)) * u - (c + self.rand_float(px)) * v)
                            to_light = current_sub_pixel - _P 
                            to_light = normalize(to_light, norm(*to_light))    
                            r = self.reflect(to_light, _n)

                            object_point =  _P + (0.00001 * to_light)
                            shadow_ray = Ray(origin=object_point, direction=to_light)
                            t, intersection, _ = self.find_intersection(shadow_ray) # testing for each object

                            if not intersection or np.dot(to_light, light.position - object_point) < t:
                                # diffuse
                                if np.dot(_n, to_light) > 0:
                                    cp += np.multiply(_object.kd * _object.color, light.intensity * np.dot(_n, to_light))

                                # specular
                                if np.dot(_v, r) > 0:
                                    cp += _object.ks * ((np.dot(_v, r) ** _object.exp) * light.intensity)
                    cp /= num_samples
        return cp

    def reflect(self, _l, _n):
        return 2 * np.dot(_n,_l) * _n - _l

    def rand_float(self, px) -> float:
        return uniform(-px, px)

