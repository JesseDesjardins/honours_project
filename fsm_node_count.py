import json

def count_nodes(folder):
    fsm_states = {}
    fsm_states_file_path = folder + 'test_result_states_fsm.txt'
    with open(fsm_states_file_path, 'r') as infile:
        fsm_states = json.load(infile)

    return len(fsm_states)

if __name__ == "__main__":
    pass