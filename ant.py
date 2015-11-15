import math
import random
import numpy as np
BETA = 1
ALPHA = 2

__author__ = 'Waner Miranda'
__email__ = 'waner@dcc.ufmg.br'


class Ant:
    def __init__(self, solver):
        self._start = solver.get_start()
        self._end = solver.get_end()
        self._solver = solver
        self._path = [solver.get_start()]
        self._path_weight = 0.0
        self._moves_weight = 0.0
        self._vertex_visited = set(self._path)
        self._moves, self._weights, self._taus = [], [], []

    def get_position(self):
        return self._path[-1]

    def get_path_weight(self):
        return self._path_weight

    def get_path(self):
        return self._path

    def step_ahead(self):
        self._moves = []
        self.get_moves()

        while len(self._moves) == 0:
            self.step_back()
            self.get_moves()

        self.calc_moves_weight()

        self.calc_nest_step()

        return None if self._path[-1] == self._end else self._path[-1]

    def get_moves(self):
        self._moves, self._weights, self._taus = self._solver.get_possible_moves(self.get_position(),
                                                                                 self._vertex_visited)

    def calc_moves_weight(self):
        self._moves_weight = 0
        for pos in range(len(self._moves)):
            vertex = self._moves[pos]
            if vertex not in self._vertex_visited:
                self._moves_weight += self._weights[pos]
        return self._moves_weight

    def calc_nest_step(self):
        sum_factors = 0
        weighted_factors = []
        for pos in range(len(self._moves)):
            weighted_eta = math.pow(self._weights[pos] / self._moves_weight, ALPHA)
            weighted_tau = math.pow(self._taus[pos], BETA)
            factor = weighted_eta * weighted_tau
            sum_factors += factor
            weighted_factors.append(factor)

        if not (sum_factors > 0):
            print "Erro sum factors"

        assert sum_factors > 0

        moves_prob = np.array(weighted_factors) / sum_factors

        selected = -1

        while selected == -1:
            for pos in range(len(self._moves)):
                chance = random.random()
                if chance <= moves_prob[pos]:
                    selected = pos
                    break

        self.move_to(pos)
        return selected

    def move_to(self, pos):
        vertex = self._moves[pos]
        self._vertex_visited.add(vertex)
        self._path.append(vertex)
        self._path_weight += self._weights[pos]
        print vertex, self._weights[pos], self._path_weight

    def step_back(self):
        last = self._path[-1]
        second_last = self._path[-2]
        weight = self._solver.get_weight(second_last, last)

        if weight is None:
            print "Error on step back"

        assert weight is not None
        self._path_weight -= weight

        self._vertex_visited.remove(last)
        del self._path[-1]


