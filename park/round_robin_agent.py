class RoundRobinAgent(object):
  def __init__(self, state_space, action_space, *args, **kwargs):
    self.state_space = state_space
    self.action_space = action_space
    self.selected = 0

  def get_action(self):
    self.selected = self.selected + 1
    act = self.selected % self.action_space.n

    return act