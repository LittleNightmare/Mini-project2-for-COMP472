from enums import Direction, Orientation
from model.car import Car


class Board(object):
    def __init__(self, line=None, h=6, w=6, create_init_board=True):
        self.height = h
        self.width = w
        self.board = []
        self.line = line
        if create_init_board:
            self._generate_board()
        self.cars: {str: Car} = {}
        self.remove_car: {str: Car} = {}
        self.key_car = None
        self.action = None
        self.moved_count = 0

    def __lt__(self, other):
        """Compare the current board with another board"""
        return self.moved_count < other.moved_count

    def __copy__(self):
        """Copy the current board"""
        new_board = Board(line=(self.line + " "), h=self.height, w=self.width, create_init_board=False)
        new_board.key_car = self.key_car
        new_board.cars = self.cars.copy()
        new_board.remove_car = self.remove_car.copy()
        new_board.board = [row.copy() for row in self.board]
        new_board.moved_count = self.moved_count
        # print(f"copy result: {id(new_board)==id(self) or id(new_board.cars)==id(self.cars) or id(new_board.board)==id(self.board) or id(new_board.key_car)==id(self.key_car) or id(new_board.line)==id(self.line) or id(new_board.action)==id(self.action)}")
        return new_board

    def _generate_board(self):
        """Generate the board"""
        for i in range(self.height):
            self.board.append([])
            for j in range(self.width):
                self.board[i].append('.')

    def add_car(self, car):
        """Add a car to the board"""
        for location in car.get_occupied_locations(update=True):
            self.board[location['x']][location['y']] = car.name
        self.cars[car.name] = car
        if car.key_car:
            # print(f"Key car is {car.name}")
            self.key_car = car.name

    def is_car_movable(self, car_name, direction, steps=1):
        """Check if the car is movable"""
        if self.cars[car_name].is_movable(will_move=steps):
            if direction is Direction.FORWARD:
                return self._is_car_movable_forward(self.cars[car_name], steps)
            elif direction is Direction.BACKWARD:
                return self._is_car_movable_backward(self.cars[car_name], steps)
        return False

    def _update_line(self):
        """Convert the current board to a line"""
        line = ''.join(''.join(map(str, row)) for row in self.board)
        # for i in range(self.height):
        #     for j in range(self.width):
        #         if self.board[i][j] != 0:
        #             line += self.board[i][j]
        #         else:
        #             line += '.'
        self.line = line

    def get_line(self):
        """Get the line of the current board"""
        return self.line

    def get_h(self, i=-1):
        """Get the heuristic value"""
        if i == 1:
            return self.get_num_blocked_positions()
        elif i == 2:
            return self.get_num_blocking_vehicle()
        elif i == 3:
            constant = 7
            return self.get_num_blocking_vehicle() * constant
        elif i == 4:
            # 0.3*h2 + 0.7*h3
            constant = 7
            return 0.3 * self.get_num_blocked_positions() + 0.3 * self.get_num_blocking_vehicle() * constant
        return 0

    def get_num_blocking_vehicle(self):
        """Get the number of blocking vehicle"""
        mid_line = ''.join(map(str, self.board[2]))
        pro_line = mid_line[self.cars[self.key_car].end_position['y'] + 1:].replace('.', '')
        exist = set()
        for car_name in pro_line:
            exist.add(car_name)
        return len(exist)

    def get_num_blocked_positions(self):
        """Get the number of blocked positions"""
        mid_line = ''.join(map(str, self.board[2]))
        pro_line = mid_line[self.cars[self.key_car].end_position['y'] + 1:].replace('.', '')
        return len(pro_line)

    def __str__(self):
        """Print the board"""
        string = '\n'.join(''.join(map(str, row)) for row in self.board)

        return string

    def _is_car_movable_forward(self, car, steps):
        """Check if the car is movable forward"""
        orientation = car.get_orientation()
        if orientation is Orientation.VERTICAL:
            if car.start_position['x'] - steps >= 0:
                for i in range(1, steps + 1):
                    if self.board[car.start_position['x'] - i][car.start_position['y']] != '.':
                        return False
                return True
            return False
        elif orientation is Orientation.HORIZONTAL:
            if car.end_position['y'] + steps < self.width:
                for i in range(1, steps + 1):
                    if self.board[car.end_position['x']][car.end_position['y'] + i] != '.':
                        return False
                return True
            return False

    def _is_car_movable_backward(self, car, steps):
        """Check if the car is movable backward"""
        orientation = car.get_orientation()
        if orientation is Orientation.VERTICAL:
            if car.end_position['x'] + steps < self.height:
                for i in range(1, steps + 1):
                    if self.board[car.end_position['x'] + i][car.end_position['y']] != '.':
                        return False
                return True
            return False
        elif orientation is Orientation.HORIZONTAL:
            if car.start_position['y'] - steps >= 0:
                for i in range(1, steps + 1):
                    if self.board[car.start_position['x']][car.start_position['y'] - i] != '.':
                        return False
                return True
            return False

    def is_game_win(self):
        """Check if the game is won"""
        if self.board[2][5] == self.key_car:
            return True
        return False

    def get_child(self, car_name, direction, steps=1):
        """Get child of the current board"""
        if self.is_car_movable(car_name, direction, steps):
            # new_board = deepcopy(self)
            # new_board = Board(line=self.line, h=self.height, w=self.width, create_init_board=False)
            # new_board.key_car = self.key_car
            # new_board.cars = self.cars.copy()
            # new_board.board = self.board.copy()
            new_board = self.__copy__()

            new_board.move_car(car_name, direction, steps)
            return new_board
        return None

    def move_car(self, car_name, direction, steps):
        """Move the car on the board"""
        # new_car: Car = deepcopy(self.cars[car_name])
        new_car: Car = self.cars[car_name].__copy__(copy_occupied_location=False)
        for step in range(steps):
            if direction is Direction.FORWARD:
                new_car.move_forward()
            elif direction is Direction.BACKWARD:
                new_car.move_backward()

        for location in self.cars[car_name].get_occupied_locations():
            self.board[location['x']][location['y']] = '.'

        could_move = False
        if (new_car.orientation is Orientation.HORIZONTAL) and (not new_car.key_car):
            if new_car.end_position == {'x': 2, 'y': 5}:
                could_move = True

        for location in new_car.get_occupied_locations():
            if not could_move:
                self.board[location['x']][location['y']] = new_car.name
            else:
                self.board[location['x']][location['y']] = '.'
        if could_move:
            self.remove_car[car_name] = new_car
            del self.cars[car_name]
        else:
            self.cars[car_name] = new_car
        self.action = (new_car.name, new_car.get_direction(direction), steps)
        self._update_line()
        self.moved_count += 1

    def get_children(self):
        """Get all the children of the current board"""
        children = []
        for car in self.cars.values():
            for direction in Direction:
                for steps in range(1, car.fuel + 1):
                    child = self.get_child(car.name, direction, steps)
                    if child is not None:
                        children.append(child)
                    else:
                        break
        return children

    def moved_cars(self) -> [Car]:
        """Get the cars that moved"""
        moved_cars = []
        for name, car in self.cars.items():
            if car.used_fuel > 0:
                moved_cars.append(car)

        for name, car in self.remove_car.items():
            moved_cars.append(car)

        return moved_cars

    def moved_cars_str(self):
        """Get the cars that moved as a string"""
        moved_cars = self.moved_cars()
        string = ''
        for car in moved_cars:
            string += f" {car.name}{car.fuel - car.used_fuel}"
        return string

    def get_fuel_state(self):
        """Get the fuel state of the cars"""
        fuel_state = ''
        for name, car in self.cars.items():
            fuel_state += f" {name}:{car.fuel - car.used_fuel},"
        for name, car in self.remove_car.items():
            fuel_state += f" {name}:{car.fuel - car.used_fuel},"
        return fuel_state[:-1]
