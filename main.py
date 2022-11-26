import time

from controller.loader import Loader
from controller.soler import Solver
from os import path


if __name__ == '__main__':
    input_file = path.join(path.dirname(__file__), 'Sample', 'sample-input.txt')
    loader = Loader(input_file)
    for game in loader.games:
        print("--------------------------------------------------------------------------------")
        solver = Solver(game)
        print("\nInitial board configuration: " + game.get_line())
        print(f"!{game.moved_cars_str()}")
        print(f"{game}")
        print("Car fuel available:"+game.get_fuel_state())
        start = time.time()
        if solver.uniform_cost_search():
            end = time.time()
            print(f"\nRuntime: {round(end - start,2)} seconds")
            state = solver.solution[1][-1]
            print(f"Search path length: {solver.search_length} states")
            print(f"Solution path length: {len(solver.solution[1]) - 1} moves")
            short_path, detail_path = solver.get_solution_path()
            print(f"Solution path: {short_path}")
            print(f"\n{detail_path}")
            print(f"\n!{state.moved_cars_str()}")
            print(state)
        else:
            end = time.time()
            print("No solution found")
            print(f"\nRuntime: {round(end - start,2)} seconds")
        # break

    # game = loader.games[1]
    # solver = Solver(game)
    # start_time = time.time()
    # if solver.uniform_cost_search():
    #     end_time = time.time()
    #     state = solver.solution[1][-1]
    #     print(solver.logs)
    #     print(state)
    #     print(f"Time: {end_time - start_time} seconds")
    # else:
    #     end_time = datetime.datetime.now()
    #     print(f"Time: {end_time - start_time} seconds")


