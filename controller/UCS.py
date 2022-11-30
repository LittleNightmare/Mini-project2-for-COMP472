from queue import PriorityQueue

from controller.solver import Solver
from enums import Status
from model.board import Board


class UCS(Solver):
    def __init__(self, board: Board):
        super().__init__(board)

    def search(self):
        """Uniform cost search"""
        # create a priority queue
        queue = PriorityQueue()
        # create a set to store visited nodes
        visited = []
        # create a node with the initial state
        # (cost, board, parent)
        f, g, h = 0, 0, 0
        node = (g, [self.board])
        # push the node into the queue
        queue.put(node)

        # loop until the queue is empty
        while not queue.empty():

            # pop the first node from the queue
            node = queue.get()
            # set old cost to g
            old_cost = node[0]
            g = old_cost
            f = g + h
            # get the current state
            state: Board = node[1][-1]
            log = f"{f} {g} {h} {state.get_line()}{state.moved_cars_str()}"
            # print(log)
            self.logs += log + "\n"
            # check if the state is the goal state
            if state.is_game_win():
                self.solution = node
                self.status = Status.SOLVED
                self.search_length = len(visited)
                return True
            # mark the state as visited
            visited.append(state.get_line())
            # get all the children of the current state
            children: [Board] = state.get_children()
            # loop through each child
            for child in children:

                path = node[1].copy()
                new_cost = len(path)
                child_line = child.get_line()
                # create a node for the child
                path.append(child)
                new_node = (new_cost, path)
                # check if the child is in the queue
                in_queue = False
                index = None
                for i, q in enumerate(queue.queue):
                    if q[1][-1].get_line() == child_line:
                        in_queue = True
                        index = i
                        break

                # if not in_queue and len(visited.intersection(child_line)) == 0:
                if not in_queue and child_line not in visited:
                    # push the node into the queue
                    queue.put(new_node)
                elif in_queue:
                    # get the node from the queue
                    old_node = queue.queue[index]
                    # get the old cost
                    old_cost = old_node[0]
                    # check if the new cost is less than the old cost
                    if new_cost < old_cost:
                        # replace the old node with the new node
                        queue.queue.pop(index)
                        queue.put(new_node)
        self.search_length = len(visited)
        self.status = Status.FAILURE
        return False
