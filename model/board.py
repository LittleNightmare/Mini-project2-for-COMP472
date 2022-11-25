from enums import Direction, Orientation


class Board(object):
    def __init__(self, line=None, h=6, w=6):
        self.height = h
        self.width = w
        self.board = []
        self.line = line
        self._generate_board()
        self.cars = {}

    def _generate_board(self):
        """Generate the board"""
        for i in range(self.height):
            self.board.append([])
            for j in range(self.width):
                self.board[i].append(0)

    def add_car(self, car):
        """Add a car to the board"""
        for location in car.get_occupied_locations():
            self.board[location['y']][location['x']] = car.name
        self.cars[car.name] = car

    def is_car_movable(self, car_name, direction, steps=1):
        """TODO: Check if the car is movable"""
        if self.cars[car_name].is_movable(will_move=steps):
            if direction is Direction.FORWARD:
                return self._is_car_movable_forward(self.cars[car_name], steps)
            elif direction is Direction.BACKWARD:
                return self._is_car_movable_backward(self.cars[car_name], steps)
        return False

    def __str__(self):
        """Print the board"""
        string = ''
        fuels = 'Car fuel available: '
        alter_fuels = '!'
        for j in range(self.height):
            for i in range(self.width):
                if self.board[i][j] != 0:
                    string += self.board[i][j]
                    if self.board[i][j] not in fuels:
                        fuels += f"{self.board[i][j]}:{self.cars[self.board[i][j]].fuel}, "
                    if self.cars[self.board[i][j]].fuel != 100 and self.board[i][j] not in alter_fuels:
                        alter_fuels += f" {self.board[i][j]}{self.cars[self.board[i][j]].fuel}"
                else:
                    string += "."
            string += '\n'
        if fuels != 'Car fuel available: ':
            string += '\n'+fuels
        return string+'\n'

    def _is_car_movable_forward(self, car, steps):
        """Check if the car is movable forward"""
        orientation = car.get_orientation()
        if orientation is Orientation.VERTICAL:
            if car.start_position['y'] + steps < self.height:
                for i in range(1, steps + 1):
                    if self.board[car.start_position['y'] + i][car.start_position['x']] != 0:
                        return False
                return True
            return False
        elif orientation is Orientation.HORIZONTAL:
            if car.end_position['x'] + steps < self.width:
                for i in range(1, steps + 1):
                    if self.board[car.end_position['y']][car.end_position['x'] + i] != 0:
                        return False
                return True
            return False

    def _is_car_movable_backward(self, car, steps):
        """Check if the car is movable backward"""
        orientation = car.get_orientation()
        if orientation is Orientation.VERTICAL:
            if car.end_position['y'] - steps >= 0:
                for i in range(1, steps + 1):
                    if self.board[car.end_position['y'] - i][car.end_position['x']] != 0:
                        return False
                return True
            return False
        elif orientation is Orientation.HORIZONTAL:
            if car.start_position['x'] - steps >= 0:
                for i in range(1, steps + 1):
                    if self.board[car.start_position['y']][car.start_position['x'] - i] != 0:
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
