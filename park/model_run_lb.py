import numpy as np
import sys
import park
import os
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.optimizers import Adam
from rl.agents import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory
from train_with_dqn import build_model, build_agent

def main(model_name):
    env_name = 'load_balance'
    env = park.make(env_name)
    states = env.observation_space.shape[0]
    actions = env.action_space.n
    model = build_model(states, actions)
    model.summary()
    dqn = build_agent(model, actions)
    dqn.compile(Adam(lr=1e-4), metrics=['mae'])
    dqn.load_weights(os.path.join(f'dqn_lb_{model_name}', "model.h5f"))
    scores = dqn.test(env, nb_episodes=1)
    print(f"score: {scores}")

if __name__ == '__main__':
    model_name = sys.argv[1]
    main(model_name)