import json
import time
import os

from load_render import load_render
from traces_to_trie import traces_to_trie

def gen_state_trie(agent_folder, num_traces=3, trace_len=1000, render_trace=True, folder_title_appending=''):
    results_dir = 'state_tries/{}/{}_traces_trie{}/'.format(agent_folder, num_traces, folder_title_appending)
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

if __name__ == "__main__":
    pass