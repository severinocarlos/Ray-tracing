from math import sqrt, inf
from modules.ray import Ray
import numpy as np

class Object:
    def __init__(self, _objects) -> None:
        self.objects = _objects
    def intersect(self):
        '''This funtion will be recreated for other class'''
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
        distance = sqrt(np.dot(ray_to_sphere, ray_to_sphere) -  t_min**2)

        if distance ** 2 <= self.radius ** 2: # d**2 <= radius**2?
            h = sqrt(distance ** 2 + self.radius ** 2) # pitagoras
            tl, tr = t_min - h, t_min + h
            if tl < 0:
                return tr if tr > 0 else inf
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
        epslon = 0.0000001

        if abs(v) < epslon:
            return inf
        else:
            h = np.dot(self.point - ray.origin, self.v_normal)
            t_parameter = h / v
            return inf if t_parameter < 0 else t_parameter


class Triangle(Object):

    def __init__(self, objects, coords: list[list], color, _h_b = 0, _h_c = 0) -> None:
        super().__init__(objects)
        self.point_A, self.point_B, self.point_C = coords
        self.color = color
        self.h_b = _h_b
        self.h_c = _h_c

    def intersect(self, ray: Ray):
        # calculating normal vector to the plane
        v = np.subtract(self.point_B, self.point_A)
        u = np.subtract(self.point_C - self.point_A)
        normal = np.cross(u,v)

        # pre processing
        projection = lambda a, b : (np.dot(a, b) / np.dot(b, b)) * b
        self.h_b = u - projection(u,v)
        self.h_c = v - projection(v,u)

        self.h_b = (np.dot(self.h_b, self.h_b) ** -1) * self.h_b
        self.h_c = (np.dot(self.h_c, self.h_c) ** -1) * self.h_c
        
        # plane intersection function
        k = np.dot(ray.direction, normal)
        
        epslon = 1e-6
        if abs(k) < epslon:
            t =  inf
        else:
            h = np.dot(self.point_A - ray.origin, self.normal) # é com o point A?
            t_parameter = h / k
            t = t_parameter if t_parameter > 0 else inf
        
        return inf if t == inf else ...

        # calculation intersection
        P = ray.origin + t * ray.direction
        vector_v = P - self.point_A
        beta = vector_v * self.h_b
        gama =  vector_v * self.h_c
        alpha = 1 - (beta + gama)

        if 0 <= alpha + beta + gama <= 1:
            return t # return escalar
        else:
            return inf