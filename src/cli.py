import argparse
import json
import os

def cli() -> list():
    parser = argparse.ArgumentParser()

    parser.add_argument('-j', '--json-file', type=str, required=True,
                        help='Escreve o json correpondente a imagem que será processada')
    parser.add_argument('-v', '--version', type=int, required=True,
                        help='Digite a versão')

    arg = parser.parse_args()
    _path = arg.json_file
    _version =  arg.version

    return [_path, _version]

if __name__ == "__main__":
    path, version = cli()
    directory = os.getcwd()
    path = f'{directory}\\items\\{path}'

    with open(path, 'r') as json_file:
        info = json.load(json_file)
