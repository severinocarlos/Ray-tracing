from .objects import Object, Sphere, Plane, Triangle
import numpy as np

# identify objects
def set_elements(objects):
    object_list = []
    for object in objects:
        if 'sphere' in object:
            new = Sphere(objects, object['sphere']['center'], object['sphere']['radius'], np.array(object['color'])/255)
        elif 'plane' in object:
            new = Plane(objects, object['plane']['sample'], object['plane']['normal'], np.array(object['color'])/255)
        else:
            new = Triangle(objects, object['triangle'], np.array(object['color'])/255) 
        object_list.append(new)
    
    return object_list