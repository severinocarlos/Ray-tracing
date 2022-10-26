from PIL import Image as ImagePil
import numpy as np

class Image:
    
    def __init__(self, height, width, background_color) -> None:
        self.height = height
        self.width = width
        self.backgroud_color = tuple(background_color)
        self.pixel_grid = [[() for __ in range(self.width)] for _ in range(self.height)]

    def set_pixel_color(self,i: int, j: int , color: tuple):
        self.pixel_grid[i][j] = color

    def draw_image(self):
        pixel_grid = np.array(self.pixel_grid)
        my_image = ImagePil.fromarray(pixel_grid, mode="RGB")
        my_image.save('2.jpg')