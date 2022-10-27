from PIL import Image as ImagePil
import numpy as np

class Color:
    def __init__(self, color) -> None:
        self.color = color



class Image(Color):    
    def __init__(self, height, width, background_color) -> None:
        self.height = height
        self.width = width
        self.backgroud_color = tuple(background_color)
        self.pixel_grid = [[self.backgroud_color for __ in range(self.width)] for _ in range(self.height)] # tá transformando em um array 3d

    def set_pixel_color(self,i: int, j: int , color: tuple):
        self.pixel_grid[i][j] = color

    def draw_image(self):
        pixel_grid = np.array(self.pixel_grid)
        print(pixel_grid)
        my_image = ImagePil.fromarray(pixel_grid, mode="RGB")
        my_image.save('2.jpg')