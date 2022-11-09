from PIL import Image as ImagePil
import numpy as np
import os

class Image():    
    def __init__(self, height, width, background_color) -> None:
        self.height = height
        self.width = width
        self.backgroud_color = background_color
        self.pixel_grid = [[self.backgroud_color for __ in range(self.width)] for _ in range(self.height)] # tá transformando em um array 3d

    def set_pixel_color(self,i: int, j: int , color: list):
        self.pixel_grid[i][j] = color

    def draw_image(self, file):
        pixel_grid = np.array(self.pixel_grid).astype(np.uint8)

        print(f'Resolution: {np.shape(pixel_grid)}')
        
        my_image = ImagePil.fromarray(pixel_grid)
        
        directory = os.getcwd()
        path = f'{directory}\\outputs\\{file[:-5]}-out-antialiasing.png'
        my_image.save(path)
        