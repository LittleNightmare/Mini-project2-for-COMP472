from controller.loader import Loader
from controller.soler import Solver
from os import path

if __name__ == '__main__':
    input_file = path.join(path.dirname(__file__), 'Sample', 'sample-input.txt')
    loader = Loader(input_file)
    # for game in loader.games:
    #     solver = Solver(game)
    #     if solver.uniform_cost_search():
    #         # print(solver.logs)
    #         state = solver.solution[1][len(solver.solution[1]) - 1]
    #         print(state)
    #     break
    game = loader.games[1]
    solver = Solver(game)
    if solver.uniform_cost_search():
        state = solver.solution[1][-1]
        print(state)


