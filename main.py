from controller.loader import Loader
from os import path

if __name__ == '__main__':
    input_file = path.join(path.dirname(__file__), 'Sample', 'sample-input.txt')
    loader = Loader(input_file)
    for game in loader.games:
        print(game)
