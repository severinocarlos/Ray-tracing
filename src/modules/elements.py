from .objects import Object, Sphere, Plane, Triangle


# identify objects
def set_elements(objects):
    object_list = []
    for object in objects:
        if 'sphere' in object:
            new = Sphere(objects, object['sphere']['center'], object['sphere']['radius'], object['color'])
        elif 'plane' in object:
            new = Plane(objects, object['plane']['sample'], object['plane']['normal'], object['color'])
        else:
            new = Triangle(objects, object['triangle'], object['color']) 
        object_list.append(new)
    
    return object_list