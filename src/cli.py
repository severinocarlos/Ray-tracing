import argparse
import json
import os
from build import Build

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

if __name__ == "__main__":
    file = cli()
    scene_info = readinfo(file)

    pixel_screen = Build(scene_info)