import numpy as np

class Light:
    def __init__(self, _intensity, _position, a1, a2, a3, a4) -> None:
        self.intensity = _intensity
        self.position = np.array(_position)
        self.a1 = a1
        self.a2 = a2
        self.a3 = a3
        self.a4 = a4