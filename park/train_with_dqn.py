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

total_training_steps=50000

def sPrint(prefix, msg):
    print(prefix)
    print(msg)


# Build training model
def build_model(states, actions):
    model = Sequential()
    model.add(Flatten(input_shape=(1, states)))
    model.add(Dense(24, activation='relu'))
    model.add(Dense(24, activation='relu'))
    model.add(Dense(actions, activation='linear'))
    return model


# Build model agent
def build_agent(model, actions):
    policy = BoltzmannQPolicy()
    memory = SequentialMemory(limit=50000, window_length=1)
    dqn = DQNAgent(model=model, memory=memory, policy=policy, nb_actions=actions, 
                    nb_steps_warmup=10000, target_model_update=1e-4)
    return dqn


# Main Entry for LB model training
def train_and_save(env, states, actions, model_name):
    model = build_model(states, actions)
    model.summary()

    dqn = build_agent(model, actions)
    dqn.compile(Adam(lr=1e-4), metrics=['mae'])
    dqn.fit(env, nb_steps=total_training_steps, visualize=True, verbose=1)
    # Save the trained model    
    dqn.save_weights(os.path.join(os.getcwd(), f'dqn_lb_{model_name}', "model.h5f"), overwrite=True)


def main(model_name):
    env_name = 'load_balance'
    env = park.make(env_name)
    states = env.observation_space.shape[0]
    actions = env.action_space.n
    sPrint("states", states)      # [load_server_1, load_server_2, ..., load_server_n, job_size] - By default 10 server + job_size
    sPrint("actions", actions)    # By default actions is 10 (i.e. 10 servers - any package can be send to)

    train_and_save(env, states, actions, model_name)

if __name__ == '__main__':
    model_name = sys.argv[1]
    main(model_name)