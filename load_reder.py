import os

import gym
import numpy as np
from datetime import datetime

from stable_baselines3 import PPO

def load_reder(folder):
    # load the best agent model
    best_model_save_dir = 'training_results/{}/best_model/'.format(folder)
    best_model = PPO.load(best_model_save_dir + 'best_model')
    
    # Enjoy tained agent and save a GIF
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
    img = env.render(mode='rgb_array')

    frame_count = 1000
    for i in range(frame_count):
        images[i] = img
        action, _states = best_model.predict(obs)
        actions.append(action)
        obs, rewards, dones, info = env.step(action)
        img = env.render(mode='rgb_array')
    images[frame_count] = img

    trace_pairs.append((0, -1)) # no action to get to initial image
    for i in range(len(actions)):
        trace_pairs.append((i+1, actions[i]))

    trace = (trace_pairs, images)
    return trace

if __name__ == "__main__":
    # Example folder name
    folder_name = '28-10-2020-16h50'
    trace = load_reder(folder=folder_name)