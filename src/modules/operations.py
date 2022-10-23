from cmath import sqrt

def ExtractVector(x1: int, y1: int, z1: int, x2: int, y2: int, z2: int) -> tuple:
    return (x1 - x2, 
            y1 - y2,
            z1 - z2)

def EscalarProd(e: int, v: tuple) -> tuple:
    x, y, z =  v
    return (e*x, e*y, e*z)

def norm(x: int, y: int, z: int) -> tuple:
    return sqrt(x**2 + y**2 + z**2)

def normalize(v: tuple) -> tuple:
    n = norm(*v)
    x, y, z = v
    return (x/n, y/n, z/n)

def crossProduct(x1: int, y1: int, z1: int, x2: int, y2: int, z2: int) -> tuple:
    return (x1 * z2 - z1 * y2,
            z1 * x2 - x1 * z2,
            x1 * y2 - y1 - x2)
