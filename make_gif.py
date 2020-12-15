import os

import imageio
import gym
import numpy as np
from datetime import datetime

from stable_baselines3 import PPO

env_id = 'LunarLander-v2'

# load the best agent model
curr_timestamp = datetime.now().strftime("%Y-%m-%d-%Hh%M")
agent_folder = '2020-12-14-19h20'

gif_dir = 'training_results/{}/'.format(agent_folder)
best_model_save_dir = 'training_results/{}/best_model/'.format(agent_folder)
best_model = PPO.load(best_model_save_dir + 'best_model')
 
# Enjoy tained agent and save a GIF
# Save action and image for each state
images = []
actions = []
#TODO Fix "RuntimeError: Tried to step environment that needs reset" error
# env.close()
# obs = env.reset()
# Current work around: create fresh env
env = gym.make(env_id)
obs = env.reset()

# This line sometimes throws an error stemming from pyglet, unsure why:
#   site-packages/pyglet/canvas/base.py, line 106, in get_default_screen
#   return self.get_screens()[0]
# IndexError: list index out of range
img = env.render(mode='rgb_array')

for i in range(1000):
    images.append(img)
    action, _states = best_model.predict(obs)
    actions.append(action)
    obs, rewards, dones, info = env.step(action)
    img = env.render(mode='rgb_array')

imageio.mimsave(gif_dir + 'lander_ppo_' + curr_timestamp + '.gif', [np.array(img) for i, img in enumerate(images) if i%2 == 0], fps=29)