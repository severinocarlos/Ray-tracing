from .objects import Sphere, Plane, Triangle
from .light import Light
import numpy as np

# identify objects and setting objects properties
def set_elements(objects, lights):
    object_list = []
    light_list = []

    for object in objects:
        if 'sphere' in object:
            new = Sphere(objects, np.array(object['sphere']['center']), object['sphere']['radius'], np.array(object['color'])/255, \
                         object['ka'], object['kd'], object['ks'], object['exp'], object['kr'], object['kt'], object['index_of_refraction'])
        elif 'plane' in object:
            new = Plane(objects, np.array(object['plane']['sample']), np.array(object['plane']['normal']), np.array(object['color'])/255, \
                        object['ka'], object['kd'], object['ks'], object['exp'], object['kr'], object['kt'], object['index_of_refraction'])
        else:
            new = Triangle(objects, object['triangle'], np.array(object['color'])/255, \
                           object['ka'], object['kd'], object['ks'], object['exp'], object['kr'], object['kt'], object['index_of_refraction'])
        
        object_list.append(new)
    
    # setting lights
    for values in lights:
        new_light = Light(np.array(values['intensity'])/255, values['position'])
        light_list.append(new_light)

    return (object_list, light_list)