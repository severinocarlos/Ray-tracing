import numpy as np

class Light:
    def __init__(self, _intensity, _position) -> None:
        self.intensity = _intensity
        self.position = np.array(_position)