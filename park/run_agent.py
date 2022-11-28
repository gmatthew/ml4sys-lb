import park
import round_robin_agent

def run():
    env = park.make('load_balance')
    print(env.action_space.n)
    #print(env.action_space[1])
    agent = round_robin_agent.RoundRobinAgent(env.observation_space, env.action_space)
    env.run(agent)

if __name__ == '__main__':
    run()
