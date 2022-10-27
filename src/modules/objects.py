import numpy as np

class Object:
    def __init__(self, r_intensity, g_intensity, b_intensity, k_a, k_d, k_s, exp):
        self.color = np.aaray([r_intensity, g_intensity, b_intensity])
        self.k_a = k_a
        self.k_d = k_d
        self.k_s = k_s
        self.exp = exp

class Plane(Object):
    def __init__(self, r_intensity, g_intensity, b_intensity, k_a, k_d, k_s, exp, p_x, p_y, p_z, n_x, n_y, n_z):
        super().__init__(r_intensity, g_intensity, b_intensity, k_a, k_d, k_s, exp)
        self.point_on_plane = np.array([p_x, p_y, p_z])
        self.normal_vector_plane = np.array([n_x, n_y, n_z])

class Sphere(Object):
    def __init__(self, r_intensity, g_intensity, b_intensity, k_a, k_d, k_s, exp, o_x, o_y, o_z, r):
        super().__init__(r_intensity, g_intensity, b_intensity, k_a, k_d, k_s, exp)
        self.radius = r
        self.center = np.array([o_x, o_y, o_z])

class Triangle(Object):
    def __init__(self, r_intensity, g_intensity, b_intensity, k_a, k_d, k_s, exp, a_x, a_y, a_z, b_x, b_y, b_z, c_x, c_y, c_z):
        super().__init__(r_intensity, g_intensity, b_intensity, k_a, k_d, k_s, exp)
        self.a = np.array([a_x, a_y, a_z])
        self.b = np.array([b_x, b_y, b_z])
        self.c = np.array([c_x, c_y, c_z])