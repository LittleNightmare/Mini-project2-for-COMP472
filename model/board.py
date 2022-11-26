from enums import Direction, Orientation
from model.car import Car
from copy import deepcopy


class Board(object):
    def __init__(self, line=None, h=6, w=6):
        self.height = h
        self.width = w
        self.board = []
        self.line = line
        self._generate_board()
        self.cars: {str: Car} = {}

    def _generate_board(self):
        """Generate the board"""
        for i in range(self.height):
            self.board.append([])
            for j in range(self.width):
                self.board[i].append(0)

    def add_car(self, car):
        """Add a car to the board"""
        for location in car.get_occupied_locations():
            self.board[location['x']][location['y']] = car.name
        self.cars[car.name] = car

    def is_car_movable(self, car_name, direction, steps=1):
        """TODO: Check if the car is movable"""
        if self.cars[car_name].is_movable(will_move=steps):
            if direction is Direction.FORWARD:
                return self._is_car_movable_forward(self.cars[car_name], steps)
            elif direction is Direction.BACKWARD:
                return self._is_car_movable_backward(self.cars[car_name], steps)
        return False

    def to_line(self):
        """Convert the current board to a line"""
        line = ''
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] != 0:
                    line += self.board[i][j]
                else:
                    line += '.'
        return line

    def __str__(self):
        """Print the board"""
        string = ''
        fuels = 'Car fuel available: '
        alter_fuels = '!'
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] != 0:
                    string += self.board[i][j]
                    # if self.board[i][j] not in fuels:
                    #     fuels += f"{self.board[i][j]}:{self.cars[self.board[i][j]].fuel}, "
                    # if self.cars[self.board[i][j]].fuel != 100 and self.board[i][j] not in alter_fuels:
                    #     alter_fuels += f" {self.board[i][j]}{self.cars[self.board[i][j]].fuel}"
                else:
                    string += "."
            string += '\n'
        if fuels != 'Car fuel available: ':
            string += '\n' + fuels
        return string + '\n'

    def _is_car_movable_forward(self, car, steps):
        """Check if the car is movable forward"""
        orientation = car.get_orientation()
        if orientation is Orientation.VERTICAL:
            if car.start_position['x'] - steps >= 0:
                for i in range(1, steps + 1):
                    if self.board[car.start_position['x'] - i][car.start_position['y']] != 0:
                        return False
                return True
            return False
        elif orientation is Orientation.HORIZONTAL:
            if car.end_position['y'] + steps < self.width:
                for i in range(1, steps + 1):
                    if self.board[car.end_position['x']][car.end_position['y'] + i] != 0:
                        return False
                return True
            return False

    def _is_car_movable_backward(self, car, steps):
        """Check if the car is movable backward"""
        orientation = car.get_orientation()
        if orientation is Orientation.VERTICAL:
            if car.end_position['x'] + steps < self.height:
                for i in range(1, steps + 1):
                    if self.board[car.end_position['x'] + i][car.end_position['y']] != 0:
                        return False
                return True
            return False
        elif orientation is Orientation.HORIZONTAL:
            if car.start_position['y'] - steps >= 0:
                for i in range(1, steps + 1):
                    if self.board[car.start_position['x']][car.start_position['y'] - i] != 0:
                        return False
                return True
            return False

    def is_game_win(self):
        """Check if the game is won"""
        if self.board[2][5] == 0:
            return False
        car = self.cars[self.board[2][5]]
        if not car.key_car:
            return False
        return True

    def get_child(self, car_name, direction, steps=1):
        """Get child of the current board"""
        if self.is_car_movable(car_name, direction, steps):
            new_board = Board()
            new_board.height = self.height
            new_board.width = self.width
            new_board.board = [row[:] for row in self.board]
            new_board.cars = self.cars.copy()
            new_board.line = self.line
            new_board.move_car(car_name, direction, steps)
            return new_board
        return None

    def move_car(self, car_name, direction, steps):
        """Move the car on the board"""
        new_car: Car = deepcopy(self.cars[car_name])
        for step in range(steps):
            if direction is Direction.FORWARD:
                new_car.move_forward()
            elif direction is Direction.BACKWARD:
                new_car.move_backward()

        for location in self.cars[car_name].get_occupied_locations():
            self.board[location['x']][location['y']] = 0

        for location in new_car.get_occupied_locations():
            self.board[location['x']][location['y']] = new_car.name
        self.cars[car_name] = new_car

    def get_children(self):
        """Get all the children of the current board"""
        children = []
        for car in self.cars.values():
            for direction in Direction:
                for steps in range(1, car.fuel + 1):
                    child = self.get_child(car.name, direction, steps)
                    if child is not None:
                        children.append(child)
        return children

    def moved_cars(self) -> [Car]:
        """Get the cars that moved"""
        moved_cars = []
        for name, car in self.cars.items():
            if car.used_fuel > 0:
                moved_cars.append(car)

        return moved_cars

    def moved_cars_str(self):
        """Get the cars that moved as a string"""
        moved_cars = self.moved_cars()
        string = ''
        for car in moved_cars:
            string += f" {car.name}{car.fuel - car.used_fuel}"
        return string
