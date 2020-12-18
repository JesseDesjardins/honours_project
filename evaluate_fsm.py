import json
import ast
import re

def total_correct_steps(folder_path):
    ''' Given a folder path containing a trie and FSM, will compare
    the FSM against all traces in the trie and return the precision
    of the FSM in terms of correctly predicted steps. These results
    will also be written out to two output files, 'evaluation.txt' 
    and a less verbose 'condensed_evaluation.txt'.

    folder_path (String) : path to folder containing the generated
    trie and FSM to be evaluated.
    '''

    output_stream = ''
    condensed_result = ''

    trie_edges = {}
    trie_states = {}
    fsm_edges = {}
    fsm_states = {}

    correct_steps_lst = []

    trie_edges_file_path = folder_path + 'trie_edges.txt'
    trie_states_file_path = folder_path + 'trie_states.txt'
    fsm_edges_file_path = folder_path + 'test_result_edges_fsm.txt'
    fsm_states_file_path = folder_path + 'test_result_states_fsm.txt'

    with open(trie_edges_file_path, 'r') as infile:
        contents = infile.read()
        trie_edges = ast.literal_eval(contents)
    with open(trie_states_file_path, 'r') as infile:
        trie_states = json.load(infile)
    with open(fsm_edges_file_path, 'r') as infile:
        contents = infile.read()
        fsm_edges = ast.literal_eval(contents)
    with open(fsm_states_file_path, 'r') as infile:
        fsm_states = json.load(infile)

    trace_ctn = 1
    for trace_root in trie_states['-1']:
        correct_steps = 0
        missed_steps = 0
        trace_len = 0
        output_stream += 'Cheking new trace...\n'
        print('Cheking new trace...')
        curr_trace = trie_states[str(trace_root)][0]
        curr_fsm = -1
        
        # for each possible starting path in the FSM:
        for path_root in fsm_states[str(curr_fsm)]:
            output_stream += ' Checking possible FSM path...\n'
            print(' Checking possible FSM path...')
            local_correct_steps = 0
            local_missed_steps = 0
            local_trace_len = 1
            curr_fsm = path_root
            trace_end = False
            while not trace_end:
                # detect end of trace
                if len(trie_states[str(curr_trace)]) == 0:
                    trace_end = True
                else:
                    local_trace_len += 1
                    next_trace = trie_states[str(curr_trace)][0]
                    action = trie_edges[(curr_trace, next_trace)]
                    next_fsm = -1
                    for child in fsm_states[str(curr_fsm)]:
                        if fsm_edges[(curr_fsm, child)] == action:
                            local_correct_steps += 1
                            next_fsm = child
                            break
                    curr_trace = next_trace
                    if next_fsm == -1:
                        local_missed_steps += 1
                    else:
                        curr_fsm = next_fsm
            if local_trace_len > trace_len: trace_len = local_trace_len
            output_stream += '  Results for this path: {} correct steps out of {}\n'.format(local_correct_steps, trace_len)
            print('  Results for this path: {} correct steps out of {}'.format(local_correct_steps, trace_len))
            if local_correct_steps > correct_steps: 
                correct_steps = local_correct_steps
                missed_steps = local_missed_steps
        output_stream += '{} correct steps out of {}\n'.format(correct_steps, trace_len)
        condensed_result += 'Trace {}: {}/{} correct steps\n'.format(trace_ctn, correct_steps, trace_len)
        print('{} correct steps out of {}'.format(correct_steps, trace_len))
        trace_ctn += 1
        correct_steps_lst.append(correct_steps)
    with open(folder_path + 'evaluation.txt', 'w') as outfile:
        outfile.write(output_stream)
    with open(folder_path + 'condensed_evaluation.txt', 'w') as outfile:
        outfile.write(condensed_result)
    return correct_steps_lst

def total_correct_steps_against_different_traces(fsm_path, trie_path):
    ''' Given a folder path containing a trie and a seperate file 
    path containing an FSM, will compare the FSM against all traces
    in the trie and return the precision of the FSM in terms of 
    correctly predicted steps. These results will also be written 
    out to two output files, 'evaluation.txt' and a less verbose 
    'condensed_evaluation.txt'.

    fsm_path (String) : path to folder containing the generated
    FSM to be evaluated.

    trie_path (String) : path to folder containing the generated
    trie to be evaluated.
    '''

    output_stream = ''
    condensed_result = ''

    trie_edges = {}
    trie_states = {}
    fsm_edges = {}
    fsm_states = {}

    correct_steps_lst = []

    trie_edges_file_path = trie_path + 'trie_edges.txt'
    trie_states_file_path = trie_path + 'trie_states.txt'
    fsm_edges_file_path = fsm_path + 'test_result_edges_fsm.txt'
    fsm_states_file_path = fsm_path + 'test_result_states_fsm.txt'

    with open(trie_edges_file_path, 'r') as infile:
        contents = infile.read()
        trie_edges = ast.literal_eval(contents)
    with open(trie_states_file_path, 'r') as infile:
        trie_states = json.load(infile)
    with open(fsm_edges_file_path, 'r') as infile:
        contents = infile.read()
        fsm_edges = ast.literal_eval(contents)
    with open(fsm_states_file_path, 'r') as infile:
        fsm_states = json.load(infile)

    trace_ctn = 1
    for trace_root in trie_states['-1']:
        correct_steps = 0
        missed_steps = 0
        trace_len = 0
        output_stream += 'Cheking new trace...\n'
        print('Cheking new trace...')
        curr_trace = trie_states[str(trace_root)][0]
        curr_fsm = -1
        
        # for each possible starting path in the FSM:
        for path_root in fsm_states[str(curr_fsm)]:
            output_stream += ' Checking possible FSM path...\n'
            print(' Checking possible FSM path...')
            local_correct_steps = 0
            local_missed_steps = 0
            local_trace_len = 1
            curr_fsm = path_root
            trace_end = False
            while not trace_end:
                # detect end of trace
                if len(trie_states[str(curr_trace)]) == 0:
                    trace_end = True
                else:
                    local_trace_len += 1
                    next_trace = trie_states[str(curr_trace)][0]
                    action = trie_edges[(curr_trace, next_trace)]
                    next_fsm = -1
                    for child in fsm_states[str(curr_fsm)]:
                        if fsm_edges[(curr_fsm, child)] == action:
                            local_correct_steps += 1
                            next_fsm = child
                            break
                    curr_trace = next_trace
                    if next_fsm == -1:
                        local_missed_steps += 1
                    else:
                        curr_fsm = next_fsm
            if local_trace_len > trace_len: trace_len = local_trace_len
            output_stream += '  Results for this path: {} correct steps out of {}\n'.format(local_correct_steps, trace_len)
            print('  Results for this path: {} correct steps out of {}'.format(local_correct_steps, trace_len))
            if local_correct_steps > correct_steps: 
                correct_steps = local_correct_steps
                missed_steps = local_missed_steps
        output_stream += '{} correct steps out of {}\n'.format(correct_steps, trace_len)
        condensed_result += 'Trace {}: {}/{} correct steps\n'.format(trace_ctn, correct_steps, trace_len)
        print('{} correct steps out of {}'.format(correct_steps, trace_len))
        trace_ctn += 1
        correct_steps_lst.append(correct_steps)
    with open(trie_path + 'evaluation.txt', 'w') as outfile:
        outfile.write(output_stream)
    with open(trie_path + 'short_evaluation.txt', 'w') as outfile:
        outfile.write(condensed_result)
    return correct_steps_lst

def get_results_from_eval_file(file_path):
    ''' Given a path to the short_evaluation.txt file, will condense
    the information into numbers and return general data.

    Returns a list of all correct step counts, the largest correct
    step count, the smallest correct step count and the average
    correct step count.
    '''

    lst = []
    with open(file_path+'short_evaluation.txt', 'r') as infile:
        for line in infile:
            nums = re.findall(r'\d+', line)
            lst.append(int(nums[1]))
    return lst, max(lst), min(lst), sum(lst)/len(lst)


if __name__ == "__main__":
    pass