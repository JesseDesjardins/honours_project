import json
import time
import os

from load_render import load_render
from traces_to_trie import traces_to_trie
from simple_ktail import ktail

def full_test(agent_folder, num_traces=3, trace_len=1000, render_trace=True, ktail_len=2, folder_title_appending=''):
    ''' Convinience method to generate traces from a pre-trained
    agent, convert traces into a trie and run a ktail algorithm to
    generate a FSM as a represention of a behaviour model for the 
    trained agent.

    agent_folder (String)        : The date subfolder in training_results 
    containing the agent to load

    num_traces (int)             : Number of traces to generate (Default 3)

    trace_len (int)              : Number of timesteps per trace 
    (Default 1000)
    
    render_trace (bool)          : Will render the trace on True
    (Default True)

    ktail_len (int)              : Length of ktail (Default 2)

    folder_title_appending (string): Optional string to append to end of 
    results folder name (Default empty string)
    '''
    results_dir = 'ktail_results/{}/{}_traces_ktail_{}{}/'.format(agent_folder, num_traces, ktail_len, folder_title_appending)
    os.makedirs(results_dir, exist_ok=True)

    traces = []
    print('Gathering traces...')
    for i in range(num_traces):
        print('  Calculating Trace {}...'.format(i+1))
        trace = load_render(folder=agent_folder, timesteps=trace_len, render=render_trace)
        # write out action traces to file
        print('  Writing trace...')
        with open(results_dir + 'action_traces_{}.txt'.format(i+1), 'w') as outfile:
            for action in trace[0]:
                outfile.write('{}\n'.format(action))
        traces.append(trace)
    print('Complete! {} traces gathered'.format(len(traces)))

    print('Converting traces into a trie...')
    trie_states, trie_edges, trie_mappings = traces_to_trie(traces=traces)
    # write out trie to file
    print('  Writing states dict...')
    with open(results_dir + 'trie_states.txt', 'w') as outfile:
        outfile.write(json.dumps(trie_states))
    print('  Writing edges dict...')
    with open(results_dir + 'trie_edges.txt', 'w') as outfile:
        # json.dumps can't deal with tuple keys :(
        outfile.write(str(trie_edges))
    print('Complete!')

    print('Generating FSM from trie...')
    start = time.time()
    fsm_states, fsm_edges, merged_pairs = ktail(states=trie_states, edges=trie_edges, k=ktail_len)
    end = time.time()
    print('Complete! Generation took {} seconds'.format(end - start))

    print('Writing out results...')
    print('  Writing states dict...')
    with open(results_dir + 'test_result_states_fsm.txt', 'w') as outfile:
        outfile.write(json.dumps(fsm_states))
    print('  Writing edges dict...')
    with open(results_dir + 'test_result_edges_fsm.txt', 'w') as outfile:
        # outfile.write(json.dumps(fsm_edges))
        # json.dumps can't deal with tuple keys :(
        outfile.write(str(fsm_edges))
    print('  Writing merges list...')
    with open(results_dir + 'test_result_merges.txt', 'w') as outfile:
        for pair in merged_pairs:
            outfile.write(str(pair))
    print('Complete!')

if __name__ == "__main__":
    pass