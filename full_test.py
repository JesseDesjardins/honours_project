import json
import time

from load_reder import load_reder
from traces_to_trie import traces_to_trie
from simple_ktail import ktail

folder_name = '28-10-2020-16h50'
traces = []
print('Gathering traces...')
for i in range(3):
    print('  Calculating Trace {}...'.format(i+1))
    traces.append(load_reder(folder=folder_name))
print('Complete! {} traces gathered'.format(len(traces)))

print('Converting traces into a trie...')
trie_states, trie_edges, trie_mappings = traces_to_trie(traces=traces)
print('Complete!')

print('Generating FSM from trie...')
start = time.time()
fsm_states, fsm_edges, merged_pairs = ktail(states=trie_states, edges=trie_edges)
end = time.time()
print('Complete! Generation took {} seconds'.format(end - start))

print('Writing out results...')
print('  Writing states dict...')
with open('test_result_states_fsm.txt', 'w') as outfile:
    outfile.write(json.dumps(fsm_states))

print('  Writing edges dict...')
with open('test_result_edges_fsm.txt', 'w') as outfile:
    # outfile.write(json.dumps(fsm_edges))
    # json.dumps can't deal with tuple keys :(
    outfile.write(str(fsm_edges))

print('  Writing merges list...')
with open('test_result_merges.txt', 'w') as outfile:
    for pair in merged_pairs:
        outfile.write(str(pair))
print('Complete!')
