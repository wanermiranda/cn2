__author__ = 'Waner Miranda'
__email__ = 'waner@dcc.ufmg.br'

DEFAULT_TAU_VALUE = 1

class WeightedGraph(object):

    def __init__(self, evaporating_rate=0.0):
        """ initializes a graph object """
        self._graph_dict = {}
        self._graph_dict_weights = {}
        self._graph_dict_tau = {}
        self._evaporating_rate = evaporating_rate

    def vertices(self):
        """ returns the vertices of a graph """
        return list(self._graph_dict.keys())

    def edges(self):
        """ returns the edges of a graph """
        return self._generate_edges()

    def add_vertex(self, vertex):
        """ If the vertex "vertex" is not in 
            self._graph_dict, a key "vertex" with an empty
            list as a value is added to the dictionary. 
            Otherwise nothing has to be done. 
        """
        if vertex not in self._graph_dict:
            self._graph_dict[vertex] = []
            self._graph_dict_weights[vertex] = []
            self._graph_dict_tau[vertex] = []

    def add_edge(self, edge, weight):
        """ assumes that edge is of type set, tuple or list; 
            between two vertices can be multiple edges! 
        """        

        (vertex1, vertex2) = tuple(edge)

        if vertex1 in self._graph_dict:
            self._graph_dict[vertex1].append(vertex2)
            self._graph_dict_weights[vertex1].append(weight)
            self._graph_dict_tau[vertex1].append(DEFAULT_TAU_VALUE)
        else:
            self._graph_dict[vertex1] = [vertex2]
            self._graph_dict_weights[vertex1] = [weight]
            self._graph_dict_tau[vertex1] = [DEFAULT_TAU_VALUE]

    def _generate_edges(self):
        """ A static method generating the edges of the 
            graph "graph". Edges are represented as sets 
            with one (a loop back to the vertex) or two 
            vertices 
        """
        edges = []
        weights = []
        
        for vertex in self._graph_dict:
            neighbour_idx = 0
            for neighbour in self._graph_dict[vertex]:
                weight = self._graph_dict_weights[vertex][neighbour_idx]
                neighbour_idx += 1
                edges.append((vertex, neighbour))
                weights.append(weight)

        return edges, weights

    def __str__(self):
        res = "vertices: "
        for k in self._graph_dict:
            res += str(k) + " "
        res += "\nedges: "
        for edge in self._generate_edges():
            res += str(edge) + " "
        return res

    def get_edges(self, vertex, visited):
        vertices = []
        weights = []
        taus = []
        for pos, n_vertex in enumerate(self._graph_dict[vertex]):
            if n_vertex not in visited:
                vertices.append(self._graph_dict[vertex][pos])
                weights.append(self._graph_dict_weights[vertex][pos])
                taus.append(self._graph_dict_tau[vertex][pos])

        return vertices, weights, taus

    def get_weight(self, v1, v2):
        for pos, v in enumerate(self._graph_dict[v1]):
            if v2 == v:
                return self._graph_dict_weights[v1][pos]
        return None

    def update_tau(self, ant):
        path = ant.get_path()
        path_cost = ant.get_path_cost()
        for idx in range(len(path) - 1):
            src_vertex = path[idx]
            dst_vertex = path[idx + 1]
            for target_idx, target_vertex in enumerate(self._graph_dict[src_vertex]):
                if target_vertex == dst_vertex:
                    self._graph_dict_tau[src_vertex][target_idx] *= (1 - self._evaporating_rate)
                    self._graph_dict_tau[src_vertex][target_idx] += 1 - (1 / path_cost)
                    pass




