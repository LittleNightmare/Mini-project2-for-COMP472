from model.board import Board


class Node(object):
    def __init__(self, state: Board, parent=None):
        self.state = state
        self.parent: Node = parent
        if parent is None:
            self.cost = 0
            self.distance = 0
            self.h = 0
        else:
            self.distance = self._cal_g()
            self.h = self._cal_heuristic()
            self.cost = self.distance + self.h

    def __lt__(self, other):
        return self.cost < other.cost

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        return hash(self.state)

    def _cal_g(self):
        return self.parent.cost + 1

    def _cal_heuristic(self):
        """TODO:Calculate heuristic"""
        return 0
