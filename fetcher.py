import os
import json
import requests

from jinja2 import Environment, FileSystemLoader

# Replace with worker node IPs
NODES = {
   "node1": "18.237.182.63",
   "node2": "34.219.86.165"
   # "node2": "18.237.182.63"
}

CONTAINER_ID_TO_ADDRESS_PORT = {
  "container21": {"address": NODES['node2'], "port": 8080, "limit": 50},
  "container22": {"address": NODES['node2'], "port": 8081, "limit": 100},
  "container23": {"address": NODES['node2'], "port": 8082, "limit": 150},
  "container11": {"address": NODES['node1'], "port": 8080, "limit": 50},
  "container12": {"address": NODES['node1'], "port": 8081, "limit": 100},
  "container13": {"address": NODES['node1'], "port": 8082, "limit": 150},
}

CPU_KEY = 'cpu'
MEMORY_KEY = 'memory'
NAME_KEY = 'name'
PERCENTAGE_KEY = 'percentage'

environment = Environment(loader=FileSystemLoader("templates/"))
template = environment.get_template("eds.jinja")


class Fetcher:

  def __init__(self, output, logger):
    self.output = output
    self.logger = logger

  # retrieves data from the collectors
  def retrieve_stats(self):
    collected_stats = {}

    for node_name in NODES:
      ip_address = NODES[node_name]
      r = requests.get('http://' + ip_address + ':5000')
      stats = json.loads(r.text)

      collected_stats[node_name] = stats

    return collected_stats

  # returns the list of nodes
  def select_node(self, collected_stats):
    node_data_list = []

    for node_name in collected_stats:
      stats = collected_stats[node_name]
      node = stats['node'][0]

      data = {}
      data['name'] = node_name
      data[CPU_KEY] = self.replace_percentage_sign(node[CPU_KEY])
      data[MEMORY_KEY] = self.replace_percentage_sign(node[MEMORY_KEY]['percent'])

      node_data_list.append(data)

    self.logger.debug('Node Stats: {}'.format(node_data_list))
    sorted_node_list = self.selection_algorithm(node_data_list)
    return sorted_node_list[0][0]

# returns the list of containers running in the first choice node
  def select_containers(self, stats):
    container_stats = []

    
    for i in range(0, len(stats)):
      data = {}
      name = stats[i]['container']
      data['name'] = name
      data[CPU_KEY] = float(self.replace_percentage_sign(stats[i][CPU_KEY])) / CONTAINER_ID_TO_ADDRESS_PORT[name]["limit"]
      data[MEMORY_KEY] = self.replace_percentage_sign(stats[i][MEMORY_KEY]['percent'])

      container_stats.append(data)

    self.logger.debug('Container Stats: {}'.format(container_stats))
    sorted_container_list = self.selection_algorithm(container_stats)
    sorted_cont_name_list = []
    for cont in sorted_container_list:
      sorted_cont_name_list.append(cont[0])
    return sorted_cont_name_list

  # returns the top choice of stats list (container or node)
  def selection_algorithm(self, stats):
    # stats argument structure => [ { name: 'foo', cpu: 10, memory: 20}]
    cpu_stats = []
    mem_stats = []
    diff = {}

    for i in range(len(stats)):
      cpu_val = stats[i][CPU_KEY]
      cpu_stats.append(float(cpu_val))
      mem_val = stats[i][MEMORY_KEY]
      mem_stats.append(float(mem_val))

    cpu_stats.sort()
    mem_stats.sort()

    for i in range(len(stats)):
      cpu_val = stats[i][CPU_KEY]
      mem_val = stats[i][MEMORY_KEY]
      diff[stats[i]['name']] = abs(float(cpu_val) - cpu_stats[0]) + abs(float(mem_val) - mem_stats[0])

    self.logger.debug("Diff Dictionary: %s", diff)
    sorted_diff = sorted(diff.items(), key = lambda kv: kv[1])
    self.logger.debug("Sorted Diff Dictionary: %s", sorted_diff)

    return sorted_diff
    '''
    min = 10000
    min_key = 0
    for k in diff.keys():
        value = diff[k]
        if (value < min):
            min = value
            min_key = k

    ## @TODO - This should return a list instead of a sorted dictionary.
    # Returns the top choice or value at index 0

    self.logger.debug("Min Key: %s", min_key)

    return min_key
    #return sorted_list[0]
    '''
  # writes first choice node and container name to results file
  def write_results(self, template):
    tmp_output = "/tmp/fetcher-temp.yaml"

    f = open(tmp_output, "w")
    f.write(template)
    f.close()

    os.system('mv -f ' + tmp_output + " " + self.output)

  def replace_percentage_sign(self, value):
    return value.replace('%', '')

  def process(self):
    collected_stats = self.retrieve_stats();

    '''
    {'node1': {'containers': [{'container': 'container23', 'cpu': '0.02%', 'memory': {'percent': '13.30%', 'raw': '68.08MiB / 512MiB'}}, {'container': 'container22', 'cpu': '0.02%', 'memory': {'percent': '13.24%', 'raw': '67.81MiB / 512MiB'}}, {'container': 'container21', 'cpu': '0.02%', 'memory': {'percent': '12.80%', 'raw': '65.54MiB / 512MiB'}}], 'node': [{'cpu': '0.601253%', 'memory': {'percent': '5.808398%', 'raw': '15069MiB / 15998 MiB'}}]}, 'node2': {'containers': [{'container': 'container13', 'cpu': '0.02%', 'memory': {'percent': '48.07%', 'raw': '246.1MiB / 512MiB'}}, {'container': 'container12', 'cpu': '0.02%', 'memory': {'percent': '45.19%', 'raw': '231.4MiB / 512MiB'}}, {'container': 'container11', 'cpu': '0.02%', 'memory': {'percent': '47.01%', 'raw': '240.7MiB / 512MiB'}}], 'node': [{'cpu': '0.350627%', 'memory': {'percent': '8.874609%', 'raw': '14579MiB / 15998 MiB'}}]}}
    '''
    all_containers = []
    for nodeid in NODES.keys():
      all_containers = all_containers + collected_stats[nodeid]['containers']

    self.logger.debug("All Containers: %s", all_containers)

    '''
    [{'container': 'container23', 'cpu': '0.02%', 'memory': {'percent': '13.30%', 'raw': '68.08MiB / 512MiB'}}, {'container': 'container22', 'cpu': '0.02%', 'memory': {'percent': '13.24%', 'raw': '67.81MiB / 512MiB'}}, {'container': 'container21', 'cpu': '0.02%', 'memory': {'percent': '12.80%', 'raw': '65.54MiB / 512MiB'}}, {'container': 'container13', 'cpu': '0.02%', 'memory': {'percent': '48.07%', 'raw': '246.1MiB / 512MiB'}}, {'container': 'container12', 'cpu': '0.02%', 'memory': {'percent': '45.19%', 'raw': '231.4MiB / 512MiB'}}, {'container': 'container11', 'cpu': '0.02%', 'memory': {'percent': '47.01%', 'raw': '240.7MiB / 512MiB'}}]
    '''

    selected_containers = self.select_containers(all_containers)
    self.logger.debug("Selected Containers: %s", selected_containers)

    endpoints = []
    weight = len(selected_containers)
    for cont in selected_containers:
      container = CONTAINER_ID_TO_ADDRESS_PORT[cont]
      self.logger.debug("Container Info: %s", container)
      endpoints.append({'address': container['address'], 'port': container['port'], 'weight': weight})
      weight = weight - 1

    self.logger.debug("Weighted container list %s", endpoints)
    rendered_template = template.render(endpoints=endpoints)

    self.write_results(rendered_template)
