import argparse
import json
import os
from build import Build
from modules.objects import Object
from modules.identify import identify

def cli() -> str:
    parser = argparse.ArgumentParser()

    parser.add_argument('-j', '--json-file', type=str, required=True,
                        help='Escreva o arquivo json correpondente a imagem que será processada, no formato <file.json>.')

    arg = parser.parse_args()
    _file = arg.json_file

    return _file

def readinfo(_file: str) -> dict():
    directory = os.getcwd()
    path = f'{directory}\\images-info\\{_file}'
    with open(path, 'r') as json_file:
        info = json.load(json_file)
    
    return info


        # self.objects = [identify_object(object_opt) for object_opt in self.objects["objects"]]
if __name__ == "__main__":
    file: str = cli()
    scene_info: dict = readinfo(file)

    objects = identify(scene_info['objects'])
    scene_info['object_list'] = objects
    scene = Build(scene_info)
    object = Object(scene_info['objects'])
    
    scene.buildRays()