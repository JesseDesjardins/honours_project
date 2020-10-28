import gym
import numpy as np

from SaveImageAndActionEachStateCallback import SaveImageAndActionEachStateCallback

from stable_baselines3 import TD3
from stable_baselines3.common.noise import NormalActionNoise

env_id = 'LunarLanderContinuous-v2'
env = gym.make(env_id)

# Add some action noise for exploration
n_actions = env.action_space.shape[-1]
action_noise = NormalActionNoise(mean=np.zeros(n_actions), sigma=0.1 * np.ones(n_actions))

# Because we use parameter noise, we should use a MlpPolicy with layer normalization
model = TD3('MlpPolicy', env, action_noise=action_noise, verbose=0)
# Create the callback: check every 1000 steps
callback = SaveImageAndActionEachStateCallback(log_dir='tmp2/')
# Train the agent
timesteps = 200
model.learn(total_timesteps=int(timesteps), callback=callback)