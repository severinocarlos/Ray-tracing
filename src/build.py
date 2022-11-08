import numpy as np
from math import hypot, inf, sqrt
from modules.ray import Ray
from modules.image import Image
from modules.light import Light
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
        self.BACKGROUND_COLOR: list = scene_dict['background_color']
        self.OBJECTS: list = scene_dict['objects']
        self.objs: list = scene_dict['object_list']
        self.lights: list = scene_dict['lights']
        self.ambient_light: list = np.array(scene_dict['ambient_light'])/255
        self.max_depth: int = scene_dict['max_depth']

    def render_scene(self) -> Image:
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
                color = np.array(self.cast(ray, self.max_depth))
                color = color*255 / max(1, *color)
                screen.set_pixel_color(i, j, color)
        return screen

    def cast(self, ray: Ray, max_depth: int) -> list:
        cs = self.BACKGROUND_COLOR
        t, intersection, object = self.find_intersection(ray)
        
        if intersection:
            P = np.array(ray.origin + (t * ray.direction)) # intersection point
            # view vector (observer)
            v = np.array([-i for i in ray.direction])
            normal_vector = object.normal(P)
            # phong shading (primary color)
            cs = self.shade(object, P, v, normal_vector)

            if max_depth > 0:
                # direction reflected
                reflected_vector = self.reflect(v, normal_vector)
                reflected_point = P + (0.00001 * reflected_vector)
                reflected_ray = Ray(origin=reflected_point, direction=reflected_vector)
                
                try:
                    if object.kt > 0:
                        refracted_vector = self.refract(object, v, normal_vector)
                        refracted_point = P + (0.00001 * refracted_vector)
                        refracted_ray = Ray(origin=refracted_point, direction=refracted_vector)
                        cs += object.kt * self.cast(refracted_ray, max_depth-1)
                    if object.kr > 0:
                        cs += object.kr * self.cast(reflected_ray, max_depth-1)
                except:
                    cs += self.cast(reflected_ray, max_depth-1)

        return cs
    
    def find_intersection(self, ray: Ray, isIntersection = False, distance = inf):
        
        # checking the intersections for each object
        for object in self.objs:
            min_intersection = object.intersect(ray)
            if min_intersection <= distance:
                distance = min_intersection
                current_object = object
                # print(distance, current_object)
            isIntersection = True if distance != inf else False
        # print('-'*40)
        # sleep(1)
        return (distance, isIntersection, current_object)
    
    def shade(self, _object, _P, _v, _n):
        cp = np.multiply(_object.ka * _object.color, self.ambient_light)
        
        norm = lambda x, y, z : hypot(x,y,z)
        normalize = lambda a, b: a / b

        for light in self.lights:
            to_light = np.array(light.position - _P)
            to_light = normalize(to_light, norm(*to_light))
            r = self.reflect(to_light, _n)

            object_point =  _P + (0.00001 * to_light)
            shadow_ray = Ray(origin=object_point, direction=to_light)
            # print('chamei do cast')
            t, intersection, _ = self.find_intersection(shadow_ray) # testing for each object

            if not intersection or np.dot(to_light, light.position - object_point) < t:
                # diffuse
                if np.dot(_n, to_light) > 0:
                    cp += np.multiply(_object.kd * _object.color, light.intensity * np.dot(_n, to_light))

                # specular
                if np.dot(_v, r) > 0:
                    cp += _object.ks * ((np.dot(_v, r) ** _object.exp) * light.intensity)
    
        return cp

    def reflect(self, _l, _n):
        return 2 * np.dot(_n,_l) * _n - _l

    def refract(self,_object, _v, _n):
        cos = np.dot(_n, _v)

        # angle > 90
        if cos < 0:
            normal = np.array([-num for num in _n])
            # intern to extern
            idx_refraction = 1 / _object.index_of_refraction
            cos = -cos
        else:
            normal = _n
            idx_refraction = _object.index_of_refraction
        delta = 1 - (1 / (idx_refraction ** 2) * (1 - (cos ** 2)))
        if delta < 0:
            raise TotalInternalReflectionException
        else:
            return  -1/idx_refraction * _v - normal * (sqrt(delta) - (1 / idx_refraction) * cos)

class TotalInternalReflectionException:
    pass