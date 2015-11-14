""" A Python Class
A simple Python graph class, demonstrating the essential 
facts and functionalities of graphs.
"""


class WeightedGraph(object):

    def __init__(self, graph_dict={}, graph_weigths_dict={}):
        """ initializes a graph object """
        self.__graph_dict = graph_dict
        self.__graph_dict_weights = graph_weigths_dict

    def vertices(self):
        """ returns the vertices of a graph """
        return list(self.__graph_dict.keys())

    def edges(self):
        """ returns the edges of a graph """
        return self.__generate_edges()

    def add_vertex(self, vertex):
        """ If the vertex "vertex" is not in 
            self.__graph_dict, a key "vertex" with an empty
            list as a value is added to the dictionary. 
            Otherwise nothing has to be done. 
        """
        if vertex not in self.__graph_dict:
            self.__graph_dict[vertex] = []

    def add_edge(self, edge, weight):
        """ assumes that edge is of type set, tuple or list; 
            between two vertices can be multiple edges! 
        """
        edge = set(edge)
        (vertex1, vertex2) = tuple(edge)
        if vertex1 in self.__graph_dict:
            self.__graph_dict[vertex1].append(vertex2)
            self.__graph_dict_weights[vertex1].append(weight)
        else:
            self.__graph_dict[vertex1] = [vertex2]
            self.__graph_dict_weights[vertex1] = [weight]

    def __generate_edges(self):
        """ A static method generating the edges of the 
            graph "graph". Edges are represented as sets 
            with one (a loop back to the vertex) or two 
            vertices 
        """
        edges = []
        weights = []
        
        for vertex in self.__graph_dict: 
            neighbour_idx = 0
            for neighbour in self.__graph_dict[vertex]:
                weight = self.__graph_dict_weights[vertex][neighbour_idx]
                neighbour_idx += 1
                if {neighbour, vertex} not in edges:
                    edges.append({vertex, neighbour})        
                    weights.append(weight)

        return edges, weights

    def __str__(self):
        res = "vertices: "
        for k in self.__graph_dict:
            res += str(k) + " "
        res += "\nedges: "
        for edge in self.__generate_edges():
            res += str(edge) + " "
        return res


