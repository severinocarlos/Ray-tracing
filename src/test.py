from locale import normalize
import numpy as np
from math import hypot, sqrt

norm = lambda x, y, z : hypot(x,y,z)
normalize = lambda a, b: np.array([a[0]/b, a[1]/b, a[2]/b])

def norm2(x: int, y: int, z: int) -> int | float:
    return sqrt(x**2 + y**2 + z**2)

def normalize2(v: tuple) -> tuple:
    n = norm2(*v)
    x, y, z = v
    return (x/n, y/n, z/n)

x = np.array([4,2,5])
y = np.array([1,0,4])

a = x
print(a)
print(norm(*a))
print(norm2(*a))

print(normalize(a, norm(*a)))
print(normalize2(a))
