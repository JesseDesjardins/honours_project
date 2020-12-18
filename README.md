# Install Instructions
Make sure to have [Pipenv](https://pipenv.pypa.io/en/latest/basics/) installed:

    pip install pipenv

Navigate to main project folder and run the following command:

    pipenv install

Activate the Pipenv shell:

    pipenv shell

Pipenv is used to create a virtual environment setup with all the dependencies used for this project.

**IMPORTANT** Once in Pipenv shell run the following commands:

    conda install swig
    pip install box2d-py

This is to avoid an issue with some of the Gym environments.


# Running the Poject
Run all files from inside the Pipenv shell:

    pipenv shell


## Note for me
running `pipenv lock` seems to timeout unless I run it in the Pipenv shell...not sure why ¯\\_(ツ)_/¯

# File Index
These are the important files and what they do, ordered by which should be run first if cloning this repo for the first time.

### `train_save_load_render.py`
This file contains the `train_save_load_render` method which trains the RL agent used for the rest of the testing. By default it uses the `LunarLander-v2` environment and PPO. It will also display and save a GIF of the agent interacting with the environment for 1000 frames. All other script are reliant on this one running first, as it creates the agent file.

### `full_test.py`
This file contains the `full_test` method, which is what is used to run every tests once the RL agent has been trained. It is essentially a convinience scrip that uses functionality from `load_render.py`, `traces_to_trie.py` and `simple_ktail.py`.

### `load_render.py`
Loads a trained RL agent and generates a trace by running it.

### `traces_to_trie.py`
Combines any number of traces into  atrie data structure.

### `simple_ktail.py`
Converts a given trie into a FSM by compressing states.

### `evaluate_fsm`
This file contains three methods, `total_correct_steps`, `total_correct_steps_against_different_traces` and `get_results_from_eval_file`. `total_correct_steps` is the large-scale evaluation method that compares a generated FSM against all traces present in a trie. `total_correct_steps_against_different_traces` does the same, but you can use a trie located in a seperate folder. This can used in conjuction with `generate_state_trie.py`. Finally, `get_results_from_eval_file` will even further reduce the output of either of the previously mentioned correct step methods into a simplified output.

## Additional files
These are not necessary for running and testing the project but are added for convenience

### `make_gif.py`
In the event `train_save_load_render.py` throws an error during the GIF creating process, which has been known to haooen from time to time, this script can be used to quickly load a model generate attempt to generate a GIF.

### `generate_state_trie.py`
Script that can generate a trie and save it in a seperate folder.

### `fsm_node_count.py`
A simple convinience method that returns the number of nodes in a FSM.