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
        self.orientation: Orientation = None

    def __copy__(self, copy_occupied_location=True):
        """Copy the car"""
        car = Car(self.name, self.fuel, self.key_car)
        car.start_position = self.start_position.copy()
        car.end_position = self.end_position.copy()
        car.used_fuel = self.used_fuel
        car.orientation = self.orientation
        if copy_occupied_location:
            car.occupied_location = self.occupied_location.copy()
        return car

    def get_orientation(self):
        """Get the orientation of the car"""
        if self.orientation is None:
            if self.start_position['x'] == self.end_position['x']:
                self.orientation = Orientation.HORIZONTAL
            else:
                self.orientation = Orientation.VERTICAL
        return self.orientation

    def _update_occupied_locations(self):
        """Get the occupied locations of the car"""
        self.occupied_location = []
        self.get_orientation()
        if self.orientation is Orientation.HORIZONTAL:
            for i in range(self.start_position['y'], self.end_position['y'] + 1):
                self.occupied_location.append({'x': self.start_position['x'], 'y': i})
        elif self.orientation is Orientation.VERTICAL:
            for i in range(self.start_position['x'], self.end_position['x'] + 1):
                self.occupied_location.append({'x': i, 'y': self.start_position['y']})

    def get_occupied_locations(self, update=False):
        """Get the occupied locations of the car"""
        if update:
            self._update_occupied_locations()
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
            self._update_occupied_locations()
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
            self._update_occupied_locations()
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
