import json

def ktail(states, edges, k=2):
    """ Simple ktail implementation

    Using two dictionaries representing the states and edges of a
    trie graph, this ktail function will return the resulting FSM
    after running the ktial mreging algortithm.

    states : a dict representation of states of a graph, where key 
             is the state and value is a list of nodes connected by 
             outgoing edges from the state
    edges  : a dict representation of edges of a graph, where the key
             is an ordered pair of states representing the outgoing 
             and incoming states connected to the edge, respectively,
             and the value is the value of the edge
    k      : desired length of the ktail (default 2)

    Returns two dicts, states and edges, and a list, merged_pairs, 
    representing the new FSM and the successfully merged pairs of 
    states, respectively.
    """
    state_tails = {} # for states in series
    ktails = {} # for edges (pair of states) in series
    merged_pairs = [] # list of successfully merged pairs of states

    for state in states: 
        # Create a sub-graph of depth k in order to facilitate finding ktails
        # Set root of sub-graph to current state
        sub_graph = {state : states[state]}
        children = states[state]

        # Build the rest of the sub-graph
        for i in range(k-1):
            new_children = []
            for child in children:
                sub_graph[child] = states[child]
                new_children += states[child]
            children = new_children

        # Get all paths for the sub-graph of length k
        state_tails[state] = []
        ktails[state] = []
        # Helper dfs function will recursively find all paths of length k in sub-graph
        dfs(graph=sub_graph, start=state, length=k+1, paths=state_tails[state])
        
        # Transform the state paths into edge paths, which will be the ktails
        for state_tail in state_tails[state]:
            ktail = []
            for i in range(len(state_tail)-1):
                ktail.append(edges[(state_tail[i], state_tail[i+1])])
            ktails[state].append(ktail)

    # Compare all k-tails to find possible merges (identical k-tails)
    # Create a list of pairs, where the first item is the state and 
    # the second is its' ktail
    all_edges_ktails = []
    for key in ktails.keys():
        for ktail in ktails[key]:
            all_edges_ktails.append((key, ktail))

    # Create a candidate list of all pairs that can be merged
    candidate_lst = []
    for i in range(len(all_edges_ktails)):
        for j in range(i+1, len(all_edges_ktails)):
            if all_edges_ktails[i][1] == all_edges_ktails[j][1]:
                candidate_lst.append((all_edges_ktails[i], all_edges_ktails[j]))

    # Attempt to merge all possible matches form the candidate list
    while len(candidate_lst) != 0:
        pair = candidate_lst[0]
        keeper_state = pair[0][0]
        merged_state = pair[1][0]
        merged = False # flag to know if merge was successful
        # Only merge if the states are not the same (i.e. don't merge the same state)
        if keeper_state != merged_state:
            # point all incoming edges from ponting towards merged_state to pointing towards keeper_state
            incoming_edges = []
            for state in states:
                if merged_state in states[state]:
                    incoming_edges.append(state)
            for state in incoming_edges:
                if keeper_state not in states[state]: states[state].append(keeper_state)
                states[state].remove(merged_state)
            # Point all outgoing edges from coming from merged_state to coming from keeper_state
            outgoing_edges = states[merged_state]
            states[keeper_state] += outgoing_edges
            # Remove possible duplicates
            states[keeper_state] = list(dict.fromkeys(states[keeper_state]))
            del states[merged_state]
            # Replace all instances of merged_state in keys from edges dict with instances of keeper_state
            defunct_edges = []
            new_edges = []
            for edge in edges:
                if merged_state in edge:
                    defunct_edges.append(edge)
            for edge in defunct_edges:
                in_state, out_state = edge
                if in_state == merged_state: in_state = keeper_state
                if out_state == merged_state: out_state = keeper_state
                edges[(in_state, out_state)] = edges[edge]
                del edges[edge]
            merged = True
        # Remove the now merged candidate pair from the candidate list and save the record to merged_pairs
        if merged:
            merged_pairs.append(candidate_lst.pop(0))
        else:
            del candidate_lst[0]
        # Refine candidate list by removing any candidates that include the now merged state
        refined_candidate_lst = []
        for candidate in candidate_lst:
            if not(merged_state == candidate[0][0] or merged_state == candidate[1][0]): refined_candidate_lst.append(candidate)
        candidate_lst = refined_candidate_lst
    # Return the now-updated states and edges dicts
    return states, edges, merged_pairs

def dfs(graph, start, length, paths, path=[]): 
    """ Simple recursive Depth First Search

    Returns all paths of length "length" originating from first value of "start"

    graph     : full graph
    start     : current state to find path from
    length    : length of paths
    paths     : list of all paths found
    path      : current path (default [])
    """
    path = path + [start] 
    if len(path) == length:
        paths.append(path) 
    else:
        for child in graph[start]:
            dfs(graph, child, length, paths, path)   

if __name__ == "__main__":
    g_s = {-1 : [0, 5],
        0 : [1],
        1 : [2],
        2 : [3],
        3 : [4],
        4 : [],
        5 : [6],
        6 : [7],
        7 : [8],
        8 : [9],
        9 : [10],
        10 : [11],
        11 : []
    }
    g_e = {(-1, 0): -1, 
        (-1, 5): -1, 
        (0, 1): 3, 
        (1, 2): 3, 
        (2, 3): 2, 
        (3, 4): 2, 
        (5, 6): 3, 
        (6, 7): 3, 
        (7, 8): 0,
        (8, 9): 1,
        (9, 10): 3,
        (10, 11): 3,
    }

    print('===============')
    print('| Input trie: |')
    print('===============')
    print('States:')
    print(g_s)
    print('Edges:')
    print(g_e)

    fsm_states, fsm_edges, merged_pairs = ktail(states=g_s, edges=g_e)

    print('===============')
    print('| Output FSM: |')
    print('===============')
    print('States:')
    print(fsm_states)
    print('Edges:')
    print(fsm_edges)
    print('Merged pairs of states:')
    print(merged_pairs)

    with open('dummy_test.txt', 'w') as outfile:
        # outfile.write(json.dumps([{'key':k, 'value': v} for k, v in fsm_edges.iteritems()]))
        outfile.write(str(fsm_edges))
