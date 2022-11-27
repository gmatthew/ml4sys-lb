import numpy as np
import park
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
                    nb_steps_warmup=10, target_model_update=1e-2)
    return dqn


# Main Entry for LB model training
def train(env, states, actions):
    model = build_model(states, actions)
    model.summary()

    dqn = build_agent(model, actions)
    dqn.compile(Adam(lr=1e-3), metrics=['mae'])
    dqn.fit(env, nb_steps=total_training_steps, visualize=False, verbose=1)


def main():
    env_name = 'load_balance'
    env = park.make(env_name)
    states = env.observation_space.shape[0]
    actions = env.action_space.n
    sPrint("states", states)      # [load_server_1, load_server_2, ..., load_server_n, job_size] - By default 10 server + job_size
    sPrint("actions", actions)    # By default actions is 10 (i.e. 10 servers - any package can be send to)

    train(env, states, actions)

if __name__ == '__main__':
    main()