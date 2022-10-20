class RoundRobinLB:
  def __init__(self, hosts):
    self.hosts = hosts
    self.hostsCount = len(self.hosts)
    self.selected = 0

  def get_host(self):
    self.selected = self.selected + 1
    return self.hosts[self.selected % self.hostsCount]

