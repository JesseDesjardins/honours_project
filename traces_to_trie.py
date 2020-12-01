import json

def traces_to_trie(traces):
    """ Will take a list of traces and return a trie
    
    The trie represented with three dictionaries, t_states, t_edges
    and t_real_states.
    
    t_states will have the state indexes as keys and the directed neighbhor
    state indexes as a list of state indexes as values for each key.

    t_edges will have ordered pairs of state indexes as keys (ordered as 
    (coming_state_index, going_state_index), represetning an edge), and the 
    corresponding value of that edge as values.

    t_real_states will have the state indexes as keys and the real state
    values (i.e. the image data) as values.

    The final trie will have a root labelled as -1, with edges
    labeled with a value of -1 that connect with the starting state
    of each trace.

    Each trace in 'traces' be a pair. Trace[0] will have an ordered 
    list of (state_index, action) pairs, and trace[1] will have an
    ordered list of states, where states[state_index] is the full 
    state image. IMPORTANT action is the incoming edge for state_index,
    not outgoing.

    Example trace:

    ([(state_index, action), (state_index, action), (state_index, action), ...], states)

    traces : A list of traces
    """
    t_states = {-1 : []}
    t_edges = {}
    t_real_states = {}
    states_index_offset = 0 # Used to maintain a unique state_index across all dicts for each state
    for trace in traces:
        last_state_index = -1
        trace_pairs = trace[0]
        states = trace[1]
        for pair in trace_pairs:
            state_index = pair[0] + states_index_offset
            action = pair[1]
            # if last_state_index != -1: last_state_index += states_index_offset
            t_states[last_state_index].append(state_index)
            # if state_index not in t_states, add it.
            if state_index not in t_states: t_states[state_index] = []
            t_edges[(last_state_index, state_index)] = action
            t_real_states[state_index] = states[state_index - states_index_offset]
            last_state_index = state_index
        states_index_offset += len(states)
    return t_states, t_edges, t_real_states

if __name__ == "__main__":
    traces = [
        ([(0, -1), (1, 3), (2, 1), (3, 0), (4, 2)], {0: 'state_a', 1:'state_b', 2:'state_c', 3:'state_d', 4:'state_e'}),
        ([(0, -1), (1, 2), (2, 0), (3, 3), (4, 2)], {0: 'state_f', 1:'state_g', 2:'state_h', 3:'state_i', 4:'state_j'}),
        ([(0, -1), (1, 1), (2, 1), (3, 2), (4, 1)], {0: 'state_k', 1:'state_l', 2:'state_m', 3:'state_n', 4:'state_o'}),
    ]
    trie_states, trie_edges, trie_mappings = traces_to_trie(traces)

    print('  Writing trie_states dict...')
    with open('test_result_trie_states.txt', 'w') as outfile:
        outfile.write(json.dumps(trie_states))
    
    print('  Writing trie_edges dict...')
    with open('test_result_trie_edges.txt', 'w') as outfile:
        outfile.write(json.dumps(trie_edges))
