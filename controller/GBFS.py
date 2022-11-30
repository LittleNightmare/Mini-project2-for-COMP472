from queue import PriorityQueue

from controller.solver import Solver
from enums import Status
from model.board import Board


class GBFS(Solver):
    def __init__(self, board: Board, heuristic=1):
        super().__init__(board)
        self.heuristic = heuristic

    def search(self):
        """Greedy Best First Search"""
        queue = PriorityQueue()
        visited = []
        f, g, h = 0, 0, self.board.get_h(self.heuristic)
        node = (h, [self.board])
        queue.put(node)
        while not queue.empty():
            node = queue.get()
            old_cost = node[0]
            h = old_cost
            f = h
            state: Board = node[1][0]
            log = f"{f} {g} {h} {state.get_line()}{state.moved_cars_str()}"
            # print(log)
            self.logs += log + "\n"
            if state.is_game_win():
                self.solution = node
                self.status = Status.SOLVED
                self.search_length = len(visited)
                return True
            visited.append(state.get_line())
            children: [Board] = state.get_children()
            for child in children:
                path = node[1].copy()
                new_cost = child.get_h(self.heuristic)
                child_line = child.get_line()
                # path.append(child)
                new_node = (new_cost, [child] + path)
                in_queue = False
                index = None
                for i, item in enumerate(queue.queue):
                    if item[1][0].get_line() == child_line:
                        in_queue = True
                        index = i
                        break
                if child_line not in visited and not in_queue:
                    queue.put(new_node)
                elif in_queue and new_cost == queue.queue[index][0]:
                    old_node = queue.queue[index]
                    if len(new_node[1]) < len(old_node[1]):
                        queue.queue.pop(index)
                        queue.put(new_node)
                elif in_queue and new_cost < queue.queue[index][0]:
                    queue.queue.pop(index)
                    queue.put(new_node)
        self.search_length = len(visited)
        self.status = Status.FAILURE
        return False

    def get_path(self):
        if self.status == Status.SOLVED:
            path = self.solution[1][:-1]
            path.reverse()
            return path
        return None
