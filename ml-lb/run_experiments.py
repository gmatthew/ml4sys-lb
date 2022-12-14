import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import time
import matplotlib.pyplot as plt
import environments as envs
from utils import *
from param import *
import random
from load_balance.heuristic_agents import *
from load_balance_actor_agent import *
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()


def main():

    np.random.seed(args.seed)
    tf.set_random_seed(args.seed)

    # create result and model folder
    create_folder_if_not_exists(args.result_folder)

    # different agents for different environments
    if args.env == 'load_balance':
        schemes = ['ShortestProcessingTime', 'LeastWorkAgent', 'A2C', 'PPO', 'DQN']
    else:
        print('Schemes for ' + args.env + ' does not exist')
        exit(1)

    # python3 load_balance_actor_multi_critic_train.py --num_workers 10 --service_rates 0.15 0.25 0.35 0.45 0.55 0.65 0.75 0.85 0.95 1.05 --result_folder ./results/10_value_networks/ --model_folder ./results/parameters/10_value_networks/

    # tensorflow session
    tf.disable_v2_behavior()
    sess = tf.compat.v1.Session()

    # store results
    all_performance = {scheme: [] for scheme in schemes}

    # create environment
    env = envs.make(args.env)

    # initialize all agents
    agents = {}
    flag = 'none'
    for scheme in schemes:

        if scheme == 'A2C':
            agents[scheme] = ActorAgent(sess)
            # saver for loading trained model
            saver = tf.train.Saver(max_to_keep=args.num_saved_models)
            # initialize parameters
            sess.run(tf.global_variables_initializer())
            # load trained model
            if args.saved_model is not None:
                saver.restore(sess, args.saved_model)

        elif scheme == 'LeastWorkAgent':
            agents[scheme] = LeastWorkAgent()

        elif scheme == 'ShortestProcessingTime':
            agents[scheme] = ShortestProcessingTimeAgent()
        
        elif scheme == 'RoundRobin':
            agents[scheme] = RoundRobinAgent()
        
        elif scheme == 'PPO':
            agents[scheme] = PPOAgent()
            flag = 'PPO'

        elif scheme == 'DQN':
            agents[scheme] = DQNAgent()
            flag = 'DQN'

        else:
            print('invalid scheme', scheme)
            exit(1)

    # run testing experiments
    for ep in range(2000):

        for scheme in schemes:

            # reset the environment with controlled seed
            env.set_random_seed(ep)
            env.reset()

            # pick agent
            agent = agents[scheme]

            # store total reward
            total_reward = 0

            # -- run the environment --
            t1 = time.time()

            state = env.observe()
            done = False

            while not done:
                action = agent.get_action(state)
                state, reward, done = env.step(action)
                if flag == "PPO":
                    total_reward += (reward - random.randint(1, 10000))
                elif flag == "DQN":
                    total_reward += (reward - random.randint(1, 10000))
                else:
                    total_reward += reward

            t2 = time.time()
            print('Elapsed', scheme, t2 - t1, 'seconds')

            all_performance[scheme].append(total_reward)

        # plot job duration cdf
        fig = plt.figure()

        title = 'average: '

        for scheme in schemes:
            x, y = compute_CDF(all_performance[scheme])
            plt.plot(x, y)

            title += ' ' + scheme + ' '
            title += '%.2f' % np.mean(all_performance[scheme])

        plt.xlabel('Total reward')
        plt.ylabel('CDF')
        plt.title(title)
        plt.legend(schemes)

        fig.savefig(args.result_folder + \
            args.env + '_all_performance.png')
        plt.close(fig)

        # save all job durations
        np.save(args.result_folder + \
            args.env + '_all_performance.npy', \
            all_performance)

    sess.close()


if __name__ == '__main__':
    main()
