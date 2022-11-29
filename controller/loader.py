from model.board import Board
from model.car import Car
import random


class Loader(object):
    def __init__(self, file_name, is_sample=True):
        self.file_name = file_name
        self.games: [Board] = []
        if is_sample:
            lines = self._load_sample_file()
        else:
            lines = self._load_file()
        for line in lines:
            self._load_game(line)

    def _load_file(self):
        """Load the file"""
        edit_lines = []
        with open(self.file_name, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if 'x' not in line:
                    line = line[3:].replace('o', '.')
                    line, _ = line.split(' ')
                    edit_lines.append(line)
        return random.choices(edit_lines, k=50)

    def _load_sample_file(self):
        """Load the file"""
        with open(self.file_name, 'r') as file:
            lines = file.readlines()
        return lines

    def _load_game(self, line):
        """Load the game"""
        cars = {}

        if line[0] != '#' and len(line) > 1:
            n = 6
            content = line.split(' ')[0]
            content = [content[i:i+n] for i in range(0, len(content), n)]
            for i, chars in enumerate(content):
                for j, char in enumerate(chars):
                    is_main_car = False
                    if char == '.':
                        continue
                    elif char == 'A':
                        is_main_car = True

                    if char not in cars.keys():
                        cars[char] = Car(char, key_car=is_main_car)
                        cars[char].start_position = {'x': i, 'y': j}
                        cars[char].end_position = {'x': i, 'y': j}
                    else:
                        cars[char].end_position = {'x': i, 'y': j}

            game = Board()
            if len(line.split(' ')) > 1:
                fuels = line.replace('\n', '').split(' ')[1:]
                # print(line + ":\n" + str(fuels))
                for fuel in fuels:
                    if fuel == '':
                        continue
                    letter = fuel[0]
                    amount = int(fuel[1])

                    cars[letter].fuel = amount
            for car in cars.values():
                game.add_car(car)
            game._update_line()
            self.games.append(game)
