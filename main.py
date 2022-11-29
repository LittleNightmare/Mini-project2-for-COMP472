import time

from controller.loader import Loader
from controller.output import Output

from controller.UCS import UCS
from controller.GBFS import GBFS
from os import path

INPUT_FILE = path.join(path.dirname(__file__), 'rush.txt')
INPUT_FILE_SAMPLE = path.join(path.dirname(__file__), 'Sample', 'sample-input.txt')
INPUT_FILE_EXAMPLE = path.join(path.dirname(__file__), 'Sample', 'example-input.txt')
OUTPUT_PATH = path.join(path.dirname(__file__), 'output')

if __name__ == '__main__':
    input_file = INPUT_FILE_SAMPLE
    loader = Loader(input_file, is_sample=True)
    used_class = [UCS, GBFS]
    for i, game in enumerate(loader.games):
        # if i != 1:
        #     continue
        for algorithm in used_class:
            if algorithm == UCS:
                solvers = [algorithm(game)]
            else:
                solvers = [algorithm(game, h) for h in range(1, 5)]
            for solver in solvers:
                start = time.time()
                solver.search()
                end = time.time()
                output = Output(game, solver, end - start, OUTPUT_PATH, i+1)
                print(f'Game {i+1} {solver.__class__.__name__} {"h"+str(solver.heuristic) if hasattr(solver,"heuristic") else ""} {round(end-start, 2)} seconds {solver.status.value}')
                output.write_to_file()

    # break
