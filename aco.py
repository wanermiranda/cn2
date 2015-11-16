from ant import Ant
import graph as gl
import processhelper as ph

__author__ = 'Waner Miranda'
__email__ = 'waner@dcc.ufmg.br'


class Solver(object):
    def __init__(self, dataset_file, anthill_size, evaporating_rate=0.0, graph=None, best_path=(-1, 0, [])):
        print "Loading dataset_file: ", dataset_file
        self._counter = 0
        self._anthill = []
        self._anthill_size = anthill_size
        self._best_path = best_path

        if graph is None:
            self._graph = graph = gl.WeightedGraph(evaporating_rate)

            # Convert the dataset form the text file into a list of vertex and edges
            # last_sz = 0
            edges_read = 0
            header = 0
            for line in open(dataset_file):
                values = line.rstrip('\n\r').split()
                values = [float(value) for value in values]
                # Skipping the headers
                if header < 2:

                    if header == 1:
                        self._start, self._end = values
                        print self._start, self._end
                    else:
                        self._vertex_count = values[0]
                        print self._vertex_count
                    header += 1
                    continue

                if len(values) > 2:
                    vertex1 = values[0]
                    vertex2 = values[1]
                    weight = values[2]
                else:
                    vertex1 = values[0]
                    vertex2 = values[0]
                    weight = values[1]

                graph.add_vertex(vertex1)
                graph.add_edge((vertex1, vertex2), weight)
                edges_read += 1
                """
                edges, weights = graph.edges()
                assert len(edges) != last_sz
                assert len(weights) != last_sz
                last_sz = len(weights)
                """
        else:
            self._graph = graph
        print("Vertices of graph:")
        vertices = graph.vertices()
        print len(vertices)

        print("Edges of graph:")
        edges, weights = graph.edges()
        print len(weights)
        print len(edges)

        assert len(vertices) == self._vertex_count
        assert len(edges) == edges_read

        self._total_edges = len(edges)
        self._total_vertices = len(vertices)

        assert (self._start in vertices) and (self._end in vertices)

        self.prepare_iteration()

        """last_step = -1
        while last_step is not None:
            last_step = ant.step_ahead() """

    def prepare_iteration(self):
        self._anthill = []
        for pos in range(self._anthill_size):
            self._anthill.append(Ant(self))

    def get_possible_moves(self, vertex, visited):
        return self._graph.get_edges(vertex, visited)

    def get_start(self):
        return self._start

    def get_end(self):
        return self._end

    def get_weight(self, v1, v2):
        return self._graph.get_weight(v1, v2)

    def evaluate(self, part, parts, thread_id):
        # print 'Thread id:', thread_id, ' Starting:', part
        size = self._total_vertices / parts
        range_max = size * part if part != parts else self._total_vertices
        range_start = size * (part - 1)
        for ant_idx in range(range_start, range_max):
            ant = self._anthill[ant_idx]
            last_step = -1
            while last_step is not None:
                last_step = ant.step_ahead()
            if ant.get_path_cost() > self._best_path[1]:
                self._best_path = (ant_idx, ant.get_path_cost(), ant.get_path())
            self.update_tau(ant)
        # print 'thread:', thread_id, self._best_path[1]

    def update_tau(self, ant):
        self._graph.update_tau(ant)

    def get_graph(self):
        return self._graph

    def get_best_path(self):
        return self._best_path
