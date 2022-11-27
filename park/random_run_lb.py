import park

env_name = 'load_balance'
episodes = 2

def run():
    env = park.make(env_name)

    # Try episode times round
    for episode in range(1, episodes + 1):
        # Try with a random agent (i.e. directly sample from action_space)
        env.seed(episode)
        obs = env.reset()
        done = False
        score = 0

        while not done:
            action = env.action_space.sample()
            obs, reward, done, info = env.step(action)
            score += reward

        print(f'Episode: {episode} Score: {score}')

if __name__ == '__main__':
    run()