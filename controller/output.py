from os import path, makedirs

from controller.solver import Solver
from enums import Status
from model.board import Board


class Output(object):
    def __init__(self, game: Board, solver: Solver, time_taken: float, output_path: str, num: int):
        self.init_game = game
        self.solver = solver
        self.time_taken = time_taken
        self.output_path = output_path
        if not path.exists(output_path):
            makedirs(output_path)
        self.num = num

    def generate_short_info(self):
        algorithm = self.solver.__class__.__name__
        h = -1
        if algorithm != "UCS":
            self.solver: algorithm = self.solver
            h = self.solver.heuristic
        if self.solver.status is Status.FAILURE:
            sol_path = "N/A"
        sol_path = self.solver.get_path()
        string = f"{self.num},{algorithm},{'h' + str(h) if h != -1 else 'NA'},{len(sol_path)},{self.solver.search_length},{round(self.time_taken, 2)}\n"
        return string

    def generate_solution_output(self):
        string = "--------------------------------------------------------------------------------\n"
        string += "\nInitial board configuration: " + self.init_game.get_line() + "\n"
        string += f"\n!{self.init_game.moved_cars_str()}"
        string += f"\n{self.init_game}\n"
        string += f"\nCar fuel available: {self.init_game.get_fuel_state()}\n"
        if self.solver.status is Status.FAILURE:
            string += f"\nNo solution found"
            string += f"\nRuntime: {round(self.time_taken, 2)} seconds"
        else:
            string += f"\nRuntime: {round(self.time_taken, 2)} seconds"
            sol_path = self.solver.get_path()
            state = sol_path[-1]
            string += f"\nSearch path length: {self.solver.search_length} states"
            string += f"\nSolution path length: {len(sol_path)} moves"
            short_path, detail_path = self.solver.get_solution_path()
            string += f"\nSolution path: {short_path}\n"
            string += f"\n{detail_path}"
            string += f"\n!{state.moved_cars_str()}\n"
            string += str(state) + "\n"
        string += f"\n--------------------------------------------------------------------------------"
        return string

    def write_to_file(self):
        algorithm = self.solver.__class__.__name__
        file_suffix = f"{self.num}.txt"
        h = -1
        if algorithm != "UCS":
            self.solver: algorithm = self.solver
            h = self.solver.heuristic
        self._write_to_file(algorithm, file_suffix, h=h)

    def _write_to_file(self, algorithm: str, file_suffix: str, h: int = -1):
        if h == -1:
            sol_name = f"{algorithm}-sol-{file_suffix}"
            search_name = f"{algorithm}-search-{file_suffix}"
        else:
            sol_name = f"{algorithm}-h{h}-sol-{file_suffix}"
            search_name = f"{algorithm}-h{h}-search-{file_suffix}"

        with open(path.join(self.output_path, sol_name), 'w') as f:
            f.write(self.generate_solution_output())

        with open(path.join(self.output_path, search_name), 'w') as f:
            f.write(self.solver.logs)

        with open(path.join(self.output_path, "short_info.csv"), 'a') as f:
            f.write(self.generate_short_info())
