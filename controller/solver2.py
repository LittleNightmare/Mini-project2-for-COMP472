from enums import Direction, Orientation, Status
from model.board import Board
from model.car import Car
from model.node import Node
from queue import PriorityQueue


class Solver(object):
    def __init__(self, board: Board):
        self.board = board
        self.solution: Node = Node(self.board)
        self.logs = ''
        self.search_length = 0
        self.status = Status.PROCESSING

    def uniform_cost_search(self):
        """Uniform cost search"""
        # create a priority queue
        queue = PriorityQueue()
        # create a set to store visited nodes
        visited = []
        # create a node with the initial state
        node = Node(self.board)
        # push the node into the queue
        queue.put(node)

        # loop until the queue is empty
        while not queue.empty():

            # pop the first node from the queue
            node = queue.get()

            # get the current state
            state: Board = node.state
            log = f"{node.cost} {node.distance} {node.h} {state.get_line()}{state.moved_cars_str()}"
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

                child_line = child.get_line()
                # create a node for the child
                new_node = Node(child, node)
                # check if the child is in the queue
                in_queue = False
                index = None
                for i, q in enumerate(queue.queue):
                    q: Node = q
                    if q.state.get_line() == child_line:
                        in_queue = True
                        index = i
                        break

                # if not in_queue and len(visited.intersection(child_line)) == 0:
                if not in_queue and child_line not in visited:
                    # push the node into the queue
                    queue.put(new_node)
                elif in_queue:
                    # get the node from the queue
                    old_node: Node = queue.queue[index]
                    # check if the new cost is less than the old cost
                    if new_node.cost < old_node.cost:
                        # replace the old node with the new node
                        queue.queue.pop(index)
                        queue.put(new_node)
        self.status = Status.FAILURE
        return False

    def get_path(self):
        node = self.solution
        path = []
        while node.parent is not None:
            path.append(node.state)
            node = node.parent
        path.reverse()
        return path

    def get_solution_path(self):
        """Get the solution path"""
        if self.status is Status.SOLVED:
            short_path = ""
            detail_path = ""
            path = self.get_path()
            for state in path:
                name, direction, steps = state.action
                short_path += f" {name} {direction.value} {steps};"
                detail_path += f"{name} {direction.value.rjust(5)} {steps}  " \
                               f"     "
                detail_path += f"{state.cars[name].fuel - state.cars[name].used_fuel} " \
                               f"{state.get_line()} {state.moved_cars_str()}\n"
            return short_path[:-1], detail_path
        return None
