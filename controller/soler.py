from enums import Direction, Orientation
from model.board import Board
from model.car import Car
import operator


class Solver(object):
    def __init__(self, board: Board):
        self.board = board
        self.solution: [int, Board, []] = None
        self.logs = ''

    def uniform_cost_search(self):
        """Uniform cost search"""
        # create a priority queue
        queue = []
        queue_lines = []
        # create a set to store visited nodes
        visited = []
        # create a node with the initial state
        # (cost, board, parent)
        f, g, h = 0, 0, 0
        node = (g, self.board, [])
        # push the node into the queue
        queue.append(node)

        # loop until the queue is empty
        while queue:
            # sort the queue in ascending order
            queue = sorted(queue, key=operator.itemgetter(0))
            # pop the first node from the queue
            node = queue.pop(0)
            # set old cost to g
            old_cost = node[0]
            g = old_cost
            f = g + h
            # get the current state
            state: Board = node[1]
            log = f"{f} {g} {h} {state.to_line()}{state.moved_cars_str()}"
            print(log)
            self.logs += log+"\n"
            # check if the state is the goal state
            if state.is_game_win():
                self.solution = node
                return True
            # mark the state as visited
            visited.append(state.to_line())
            # get all the children of the current state
            children: [Board] = state.get_children()
            # loop through each child
            for child in children:
                new_cost = 1+old_cost
                child_line = child.to_line()
                # create a node for the child
                new_node = (new_cost, child, node)
                # check if the child is in the queue
                if child_line not in [x[1].to_line() for x in queue] and child_line not in visited:
                    # push the node into the queue
                    queue.append(new_node)
                elif child_line in [x[1].to_line() for x in queue]:
                    # get the index of the child in the queue
                    index = [x[1].to_line() for x in queue].index(child_line)
                    # get the node from the queue
                    old_node = queue[index]
                    # get the old cost
                    old_cost = old_node[0]
                    # check if the new cost is less than the old cost
                    if new_cost < old_cost:
                        # replace the old node with the new node
                        queue[index] = new_node
        return False

    def __str__(self):
        """Print the board"""
        return str(self.board)
