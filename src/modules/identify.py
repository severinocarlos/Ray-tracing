from objects import *

def identify(objects):
    object_list = []
    for object in objects:
        if 'sphere' in object:
            new = Sphere(objects, object['center'], object['radius'])
        elif 'plane' in object:
            new = Plane(objects, object['sample'], object['normal'])
        else:
            new = Triangle(objects, object['triangle']) 
        object_list.append(new)
    return object_list