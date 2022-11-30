from enums import Status
from model.board import Board


class Solver(object):
    def __init__(self, board: Board):
        self.board = board
        self.solution: [int, [Board]] = None
        self.logs = ''
        self.search_length = 0
        self.status = Status.PROCESSING

    def search(self):
        pass

    def get_path(self):
        """Get the solution path"""
        if self.status is Status.SOLVED:
            path = self.solution[1][1:]
            return path
        return None

    def get_solution_path(self):
        """Get the solution path"""
        if self.status is Status.SOLVED:
            short_path = ""
            detail_path = ""
            path = self.get_path()
            for state in path:
                name, direction, steps = state.action

                if name in state.remove_car.keys():
                    used_fuel = state.remove_car[name].fuel - state.remove_car[name].used_fuel
                else:
                    used_fuel = state.cars[name].fuel - state.cars[name].used_fuel
                short_path += f" {name} {direction.value} {steps};"
                detail_path += f"{name} {direction.value.rjust(5)} {steps}  " \
                               f"     "
                detail_path += f"{used_fuel} " \
                               f"{state.get_line()} {state.moved_cars_str()}\n"
            return short_path[:-1], detail_path
        return None
