from math import sqrt, inf, hypot
from modules.ray import Ray
import numpy as np
from time import sleep

class Object:
    def __init__(self, _objects) -> None:
        self.objects = _objects
    def intersect(self):
        '''This function will be recreated for other class'''
        pass

class Sphere(Object):
    
    def __init__(self, objects, center, radius, color, tl = 0, tr = 0) -> None:
        super().__init__(objects)
        self.center = np.array(center)
        self.radius = radius
        self.color = color
        self.tl = tl # first parameter
        self.tr = tr # second parameter

    def intersect(self, ray: Ray):
 
        ray_to_sphere = self.center - ray.origin # ray origin to sphere origin
        
        t_min = np.dot(ray_to_sphere, ray.direction) # parameter
        
        distance = sqrt(np.dot(ray_to_sphere, ray_to_sphere) -  t_min ** 2)

        if distance ** 2 <= self.radius ** 2: # d**2 <= radius**2?
            h = sqrt(self.radius ** 2 - distance ** 2) # pitagoras
            tl, tr = t_min - h, t_min + h
            if tl < 0:
                return inf if tr < 0 else tr
            else:
                return tl
        else: # not intersection
            return inf


class Plane(Object):

    def __init__(self, objects: Object, point: list, v_normal: list, color) -> None:
        super().__init__(objects)
        self.point = np.array(point)
        self.v_normal = np.array(v_normal)
        self.color = color

    def intersect(self, ray: Ray):
        v = np.dot(ray.direction, self.v_normal) 
        EPSLON = 0.0000001

        if abs(v) < EPSLON:
            return inf
        else:
            h = np.dot(self.point - ray.origin, self.v_normal)
            t_parameter = h / v
            return inf if t_parameter < 0 else t_parameter


class Triangle(Object):

    def __init__(self, objects, coords: list[list], color) -> None:
        super().__init__(objects)
        self.point_A, self.point_B, self.point_C = np.array(coords[0]), \
                                                   np.array(coords[1]), \
                                                   np.array(coords[2])
        self.color = color
        
        # calculating normal vector to the plane
        u = self.point_B - self.point_A
        v = self.point_C - self.point_A
        self.normal = np.cross(u, v)
      
        # pre processing
        projection = lambda a, b : (((np.dot(a, b)) / (np.dot(b, b))) * b)
        h_b = u - projection(u, v)       
        h_c = v - projection(v, u)

        self.h_b =  h_b / (np.dot(h_b, h_b))
        self.h_c =  h_c / (np.dot(h_c, h_c))

    def intersect(self, ray: Ray):
        # plane intersection function
        v = np.dot(ray.direction, self.normal)
        EPSLON = 0.0000001
    
        if abs(v) < EPSLON: # parallel to the plane
            t =  inf
        else:
            h = np.dot(self.point_A - ray.origin, self.normal) 
            t_parameter = h / v
            t = inf if t_parameter < 0 else t_parameter
        
        
        if t == inf: # not intersection
            return inf

        # calculation intersection point
        P = ray.origin + (t * ray.direction)
        vector_v = P - self.point_A
        beta = np.dot(vector_v, self.h_b)
        gama =  np.dot(vector_v, self.h_c)
        alpha = 1 - (beta + gama)

        if alpha < 0 or beta < 0 or gama < 0:           
            return inf 
        else:
            return t # return escalar