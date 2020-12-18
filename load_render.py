import os

import gym
import numpy as np
from datetime import datetime

from stable_baselines3 import PPO

def load_render(folder, timesteps=1000, render=True):
    ''' Loads a previously trained agent and runs it,
    generating a trace. 
    
    Each trace in 'traces' be a pair. Trace[0] will have an ordered 
    list of (state_index, action) pairs, and trace[1] will have an
    ordered list of states, where states[state_index] is the full 
    state image. IMPORTANT action is the incoming edge for state_index,
    not outgoing.

    folder (String) : The date subfolder in training_results 
    containing the agent to load

    timesteps (int) : The number of timesteps for each trace (Default
    1000)

    render (bool)   : Wether or not to render the agent while running
    trace. False will result in faster trace generation but will not
    generate real image states.
    '''
    # load the best agent model
    best_model_save_dir = 'training_results/{}/best_model/'.format(folder)

    best_model = PPO.load(best_model_save_dir + 'best_model')
    
    # Save action and image for each state
    images = {}
    actions = []
    trace_pairs = []

    env_id = 'LunarLander-v2'
    env = gym.make(env_id)
    obs = env.reset()

    # This line sometimes throws an error stemming from pyglet, unsure why:
    #   site-packages/pyglet/canvas/base.py, line 106, in get_default_screen
    #   return self.get_screens()[0]
    # IndexError: list index out of range

    img = env.render(mode='rgb_array') if render else None

    frame_count = timesteps
    for i in range(frame_count):
        images[i] = img
        action, _states = best_model.predict(obs)
        actions.append(action)
        obs, rewards, dones, info = env.step(action)
        img = env.render(mode='rgb_array') if render else None
    images[frame_count] = img

    trace_pairs.append((0, -1)) # no action to get to initial image
    for i in range(len(actions)):
        trace_pairs.append((i+1, actions[i]))

    trace = (trace_pairs, images)
    return trace

if __name__ == "__main__":
    pass