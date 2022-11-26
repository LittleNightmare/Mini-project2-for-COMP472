from enum import Enum


class Orientation(Enum):
    HORIZONTAL = 'Horizontal'
    VERTICAL = 'Vertical'


class Direction(Enum):
    FORWARD = 'Forward'
    BACKWARD = 'Backward'


class Movement(Enum):
    LEFT = 'Left'
    RIGHT = 'Right'
    UP = 'Up'
    DOWN = 'Down'


class Status(Enum):
    SOLVED = 'Solved'
    PROCESSING = 'Processing'
    FAILURE = 'No solution'
