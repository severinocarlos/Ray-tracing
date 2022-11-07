import argparse
import json
import os
from build import Build
from modules.elements import set_elements
from modules.image import Image

def cli() -> str:
    parser = argparse.ArgumentParser()

    parser.add_argument('-j', '--json-file', type=str, required=True,
                        help='Escreva o arquivo json correpondente a imagem que será processada, no formato <file.json>.')

    arg = parser.parse_args()
    _file = arg.json_file

    return _file

def readinfo(_file: str) -> dict:
    directory = os.getcwd()
    
    path = f'{directory}\\images-info\\version-2\\{_file}'
    with open(path, 'r') as json_file:
        info = json.load(json_file)
    
    return info

if __name__ == "__main__":
    file: str = cli()
    scene_info: dict = readinfo(file)
    print(scene_info)
    
    # setting object and info in the scene
    objects, lights = set_elements(scene_info['objects'], scene_info['lights'])
    scene_info['object_list'] = objects
    scene_info['lights'] = lights

    
    scene = Build(scene_info)
    # building scene elements
    image: Image = scene.buildRays()
    
    # draw the image
    image.draw_image(file)
    