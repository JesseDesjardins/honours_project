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
        """ Simple class to show a loading bar while training
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
    ''' To properly visualize the ProgressBarCallback class while
    training
    '''
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

#TODO Eventally get action and image per state WHILE training, future reseach perhaps
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

def train_save_load_render_gif(num_timesteps=10000, eval_episodes=5, eval_frequency=1000):
    ''' Large method that will create a LunarLandar-v2 RL environment,
    train and save an agent using user-specified paramenters, reload 
    the trained agent and generate a GIF of the agent in action.

    num_timesteps (int)  : number of timesteps to train over 
    (Default 10,000)
    eval_episodes (int)  : number of episodes to test the agent 
    against during the training process (Default 5)
    eval_frequency (int) : evaluate the agent during training each 
    eval_frequency many timesteps (Default 1000)
    '''

    # Create session dirs
    #TODO change date format to year-month-day-hour-minute
    curr_timestamp = datetime.now().strftime("%Y-%m-%d-%Hh%M")
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
    policy_id = 'MlpPolicy'
    model = PPO(policy_id, env)

    # Create the callback
    auto_save_callback = EvalCallback(
        eval_env=env, 
        callback_on_new_best=None, 
        n_eval_episodes=eval_episodes, 
        eval_freq=eval_frequency, 
        log_path=log_dir, 
        best_model_save_path=best_model_save_dir, 
        deterministic=True, 
        render=False, 
        verbose=1
    )

    # Train the agent
    timesteps = num_timesteps

    print('Training {} environment with PPO algorithm using {} policy over {} timesteps'.format(env_id, policy_id, timesteps))

    with ProgressBarManager(timesteps) as progress_callback:
        model.learn(total_timesteps=int(timesteps), callback=[progress_callback, auto_save_callback])

    # load the best agent model
    best_model = PPO.load(best_model_save_dir + 'best_model')

    # Enjoy trained agent and save a GIF
    # Save action and image for each state
    images = []
    actions = []

    #BUG Fix "RuntimeError: Tried to step environment that needs reset" error
    # env.close()
    # obs = env.reset()
    # Current work around: create fresh env
    env = gym.make(env_id)
    obs = env.reset()

    # BUG: This line sometimes throws an error stemming from pyglet, unsure why:
    #   site-packages/pyglet/canvas/base.py, line 106, in get_default_screen
    #   return self.get_screens()[0]
    # IndexError: list index out of range
    # If Index Error thrown, just run make_gif with the correct date folder
    img = env.render(mode='rgb_array')

    for i in range(1000):
        images.append(img)
        action, _states = best_model.predict(obs)
        actions.append(action)
        obs, rewards, dones, info = env.step(action)
        img = env.render(mode='rgb_array')

    imageio.mimsave(gif_dir + 'lander_ppo_' + str(timesteps) + '.gif', [np.array(img) for i, img in enumerate(images) if i%2 == 0], fps=29)

if __name__ == "__main__":
    train_save_load_render_gif(num_timesteps=500000, eval_episodes=5, eval_frequency=1000)