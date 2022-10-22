import argparse
import json
import os

def cli() -> tuple():
    parser = argparse.ArgumentParser()

    parser.add_argument('-j', '--json-file', type=str, required=True,
                        help='Escreve o arquivo json correpondente a imagem que será processada')

    arg = parser.parse_args()
    _file = arg.json_file
    _version =  arg.version

    return (_file, _version)

def readinfo(_file: str) -> dict():
    directory = os.getcwd()
    path = f'{directory}\\images-info\\{_file}'

    with open(path, 'r') as json_file:
        _info = json.load(json_file)
    
    return _info

if __name__ == "__main__":
    file, version = cli()
    info = readinfo(file)

    print(info)
    