import gym
import imageio
import numpy as np

from stable_baselines3 import TD3
from stable_baselines3.common.evaluation import evaluate_policy


model = TD3.load('tmp/best_model')
env = gym.make('LunarLanderContinuous-v2')

# Evaluate the agent
mean_reward, std_reward = evaluate_policy(model, env, n_eval_episodes=10)

# Make GIF
images = []
obs = env.reset()
img = env.render(mode='rgb_array')
for i in range(250):
    images.append(img)
    action, _ = model.predict(obs)
    print(action)
    obs, _, _ ,_ = env.step(action)
    img = env.render(mode='rgb_array')

imageio.mimsave('lander_td3.gif', [np.array(img) for i, img in enumerate(images) if i%2 == 0], fps=29)

# # Enjoy trained agent
# obs = env.reset()
# for i in range(1000):
#     action, _states = model.predict(obs)
#     obs, rewards, dones, info = env.step(action)
#     env.render()