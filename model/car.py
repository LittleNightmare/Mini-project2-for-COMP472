from enums import Orientation, Direction, Movement


class Car(object):
    def __init__(self, name: str, fuel=100, key_car=False):
        self.name = name
        self.key_car = key_car
        self.fuel = fuel
        self.used_fuel = 0
        self.start_position = {'x': 0, 'y': 0}
        self.end_position = {'x': 0, 'y': 0}
        self.occupied_location = []

    def get_orientation(self):
        """Get the orientation of the car"""
        if self.start_position['x'] == self.end_position['x']:
            return Orientation.HORIZONTAL
        else:
            return Orientation.VERTICAL

    def get_occupied_locations(self):
        """Get the occupied locations of the car"""
        self.occupied_location = []
        orientation = self.get_orientation()
        if orientation is Orientation.HORIZONTAL:
            for i in range(self.start_position['y'], self.end_position['y'] + 1):
                self.occupied_location.append({'x': self.start_position['x'], 'y': i})
        elif orientation is Orientation.VERTICAL:
            for i in range(self.start_position['x'], self.end_position['x'] + 1):
                self.occupied_location.append({'x': i, 'y': self.start_position['y']})
        return self.occupied_location

    def is_movable(self, will_move=0):
        """Check if the car could move"""
        return self.fuel > 0 and self.used_fuel + will_move < self.fuel

    def move_forward(self):
        """Move the car forward(up and right)"""
        if self.is_movable():
            orientation = self.get_orientation()
            if orientation is Orientation.VERTICAL:
                self.start_position['x'] -= 1
                self.end_position['x'] -= 1
            elif orientation is Orientation.HORIZONTAL:
                self.start_position['y'] += 1
                self.end_position['y'] += 1
            self.used_fuel += 1

            return True
        return False

    def move_backward(self):
        """Move the car backward(down and left)"""
        if self.is_movable():
            orientation = self.get_orientation()
            if orientation is Orientation.VERTICAL:
                self.start_position['x'] += 1
                self.end_position['x'] += 1
            elif orientation is Orientation.HORIZONTAL:
                self.start_position['y'] -= 1
                self.end_position['y'] -= 1

            self.used_fuel += 1
            return True
        return False

    def get_direction(self, direction: Direction):
        """Get the relative direction of the game"""
        orientation = self.get_orientation()
        if direction == Direction.FORWARD:
            if orientation == Orientation.VERTICAL:
                return Movement.UP
            elif orientation == Orientation.HORIZONTAL:
                return Movement.RIGHT
        elif direction == Direction.BACKWARD:
            if orientation == Orientation.VERTICAL:
                return Movement.DOWN
            elif orientation == Orientation.HORIZONTAL:
                return Movement.LEFT
