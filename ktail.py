import random

from graphs import Graph

# Automatic Steering of Behavioral Model Inference
# examples coded

# A trace is a list of tuples: index 0 is the event, index 1 is the state
huh_traces = [
        [(0, [1]), (2, [2]), (0, [3]), (2, [4]), (3, [5]), (1, [6]), (3, [7]), (1, [8]), (0, [9]), (1, [10])],
        [(2, [11]), (1, [12]), (1, [13]), (0, [14]), (2, [15]), (1, [16]), (2, [17]), (3, [18]), (2, [19]), (2, [20])],
        [(3, [21]), (3, [22]), (2, [23]), (1, [24]), (0, [25]), (0, [26]), (1, [27]), (3, [28]), (3, [29]), (0, [30])]
]

traces = [
    [3, 1, 1, 1, 0, 2, 1, 3, 1, 0],
    [0, 2, 2, 0, 3, 2, 1, 3, 2, 1],
    [2, 0, 0, 0, 1, 3, 1, 1, 1, 3]
]

paper_example = [
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
            trie.add_vertex(event)
            trie.add_edge({node, str(event)})
            node = event
    return trie

# 2) Using ktail, create refined trace list

# 3) create FSM

# counter = 0
# for _ in range (3):
#     lst = []
#     for _ in range (10):
#         lst.append(random.randint(0,3))
#     print(lst)

if __name__ == "__main__":
    trie = traces_to_trie(traces)
    print(trie)