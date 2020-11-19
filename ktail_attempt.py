# Graph class taken from https://www.python-course.eu/graphs_python.php
# with slight modifications

""" A Python Class
A simple Python graph class, demonstrating the essential 
facts and functionalities of graphs.
"""
class Graph(object):

    def __init__(self, graph_dict=None):
        """ initializes a graph object 
            If no dictionary or None is given, 
            an empty dictionary will be used
        """
        if graph_dict == None:
            graph_dict = {}
        self.__graph_dict = graph_dict

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

    def add_edge(self, edge):
        """ assumes that edge is of type set, tuple or list; 
            between two vertices can be multiple edges! 
        """
        # edge = set(edge)
        (vertex1, vertex2, event) = tuple(edge)
        if vertex1 in self.__graph_dict:
            self.__graph_dict[vertex1].append((vertex2, event))
        else:
            self.__graph_dict[vertex1] = [(vertex2, event)]

    def __generate_edges(self):
        """ A static method generating the edges of the 
            graph "graph". Edges are represented as sets 
            with one (a loop back to the vertex) or two 
            vertices 
        """
        edges = []
        for vertex in self.__graph_dict:
            for neighbour in self.__graph_dict[vertex]:
                if {neighbour, vertex} not in edges:
                    edges.append({neighbour, vertex})
        return edges

    def __str__(self):
        res = "vertices: "
        for k in self.__graph_dict:
            res += str(k) + " "
        res += "\nedges: "
        for edge in self.__generate_edges():
            res += str(edge) + " "
        return res
    
    def show_dict(self):
        return self.__graph_dict

example_traces = [
    ['UP', 'W', 'X', 'G', 'T', 'S', 'A', 'O', 'Y'],
    ['DEL', 'W', 'X', 'G', 'C', 'L', 'D', 'O', 'Y']
]

# 1) Create PTA (Trie) from traces using a dict
            
def traces_to_trie(traces):
    trie = Graph()
    trie.add_vertex('_root')
    state_number = 0 # use to autogenerate state names
    for trace in traces:
        node = '_root'
        for event in trace:
            state_number += 1
            trie.add_vertex(state_number)
            trie.add_edge((node, state_number, event))
            node = state_number
    return trie

# 2) Using ktail, create refined trace list

def ktail_merge(trie, k=2):
    vertices = trie.vertices
    # Loop through all nodes
    for i in range(len(vertices)):
        curr_node = vertices[i]
        # Get the ktail for the current node
        curr_ktail = []
        for x in range(k):
            try:
                next_node = vertices[i + x]
            except IndexError:
                break
            else:
                (_, next_event) = next_node
                curr_ktail.append(next_event)
        # Loop through all remaining nodes
        for j in range(i+1, len(vertices)):
            # Get the ktail for the node we may merge
            next_ktail = []
            for x in range(k):
                try:
                    next_node = vertices[i + x]
                except IndexError:
                    break
                else:
                    (_, next_event) = next_node
                    curr_ktail.append(next_event)
            # Compare ktails
            if curr_ktail == next_ktail:
                # Merge
                # Merge must include removing the old state
                # from the verticies list AND from any value
                # list stored in the trie dict, as well as
                # remove one from the len of the for loops
                # ...this seems like a problematic implementation
                pass


if __name__ == "__main__":
    trie = traces_to_trie(example_traces)
    print(trie)
    print('Raw dictionary: ', end='')
    print(trie.show_dict())