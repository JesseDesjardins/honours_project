import os

import imageio
import gym
import numpy as np
from datetime import datetime

from tqdm.auto import tqdm

from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.callbacks import BaseCallback, EvalCallback

# Class called by ProgressBarManager
class ProgressBarCallback(BaseCallback):
        """
        :param pbar: (tqdm.pbar) Progress bar object
        """
        def __init__(self, pbar):
            super(ProgressBarCallback, self).__init__()
            self._pbar = pbar

        def _on_step(self):
            # Update the progress bar:
            self._pbar.n = self.num_timesteps
            self._pbar.update(0)

# Nice loading bar callback (using 'with' block)
class ProgressBarManager(object):
    def __init__(self, total_timesteps): # init object with total timesteps
        self.pbar = None
        self.total_timesteps = total_timesteps
        
    def __enter__(self): # create the progress bar and callback, return the callback
        self.pbar = tqdm(total=self.total_timesteps)
            
        return ProgressBarCallback(self.pbar)

    def __exit__(self, exc_type, exc_val, exc_tb): # close the callback
        self.pbar.n = self.total_timesteps
        self.pbar.update(0)
        self.pbar.close()

#TODO Eventally get action and image per state WHILE training
# Custom Calback
class SaveActionImagePerStateCallback(BaseCallback):
    def __init__(self, info_dump_dir: str, verbose=1):
        super(SaveActionImagePerStateCallback, self).__init__(verbose)
        self.info_dump_dir = info_dump_dir

    def _init_callback(self) -> None:
        # Create folder if needed
        if self.info_dump_dir is not None:
            os.makedirs(self.info_dump_dir, exist_ok=True)
    
    def _on_step(self) -> bool:
        #TODO access actions and images DURING TRAINING and save to info_dump_dir
        return True

# Create session dirs
curr_timestamp = datetime.now().strftime("%d-%m-%Y-%Hh%M")
log_dir = 'training_results/{}/logs/'.format(curr_timestamp)
best_model_save_dir = 'training_results/{}/best_model/'.format(curr_timestamp)
gif_dir = 'training_results/{}/'.format(curr_timestamp)
os.makedirs(log_dir, exist_ok=True)
os.makedirs(best_model_save_dir, exist_ok=True)
os.makedirs(gif_dir, exist_ok=True)

# Create and wrap environment
env_id = 'LunarLander-v2'
env = gym.make(env_id)
print(env.action_space)
env = Monitor(env, log_dir)

# Create the model
model = PPO('MlpPolicy', env)

# Create the callback
auto_save_callback = EvalCallback(env, None, 5, 1000, log_dir, best_model_save_dir, True, False, 1)

# Train the agent
timesteps = 5000

with ProgressBarManager(timesteps) as progress_callback:
    model.learn(total_timesteps=int(timesteps), callback=[progress_callback, auto_save_callback])

# load the best agent model
best_model = PPO.load(best_model_save_dir + 'best_model')
 
# Enjoy tained agent and save a GIF
# Save action and image for each state
images = []
actions = []
#TODO Fix "RuntimeError: Tried to step environment that needs reset" error
# env.close()
# obs = env.reset()
# Current work around: create fresh env
env = gym.make('LunarLander-v2')
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

imageio.mimsave(gif_dir + 'lander_ppo.gif', [np.array(img) for i, img in enumerate(images) if i%2 == 0], fps=29)
print(actions)
print(images[0])