from .objects import Sphere, Plane, Triangle


# identify objects and setting objects properties
def set_elements(objects):
    object_list = []

    for object in objects:
        if 'sphere' in object:
            new = Sphere(objects, object['sphere']['center'], object['sphere']['radius'], object['color'],
                         object['ka'], object['kd'], object['ks'], object['exp'])
        elif 'plane' in object:
            new = Plane(objects, object['plane']['sample'], object['plane']['normal'], object['color'],
                        object['ka'], object['kd'], object['ks'], object['exp'])
        else:
            new = Triangle(objects, object['triangle'], object['color'],
                           object['ka'], object['kd'], object['ks'], object['exp'])
        
        object_list.append(new)
    
    return object_list