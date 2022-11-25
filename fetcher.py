import json, requests
import time

# Replace with worker node IPs
NODES = {
  "node1": "10.0.60.93",
  "node2": "10.0.60.194"
}

CPU_KEY = 'cpu'
MEMORY_KEY = 'memory'
NAME_KEY = 'name'
PERCENTAGE_KEY = 'percentage'

DATA_RETRIEVAL_INTERVAL_SECONDS = 5

def retrieve_node_stats():
  node_stats = {}

  for node_name in NODES:
    ip_address = NODES[node_name]
    r = requests.get('http://' + ip_address + ':5000')
    stats = json.loads(r.text)

    node_stats[node_name] = stats

  return node_stats

'''
returns the sort list of nodes to select from
'''


def select_node(node_stats):
  node_data_list = []

  for node_name in node_stats:
    stats = node_stats[node_name]
    node = stats['node'][0]

    data = {}
    data['name'] = node_name
    data[CPU_KEY] = replace_percentage_sign(node[CPU_KEY])
    data[MEMORY_KEY] = replace_percentage_sign(node[MEMORY_KEY]['percent'])

    node_data_list.append(data)

  return selection_algorithm(node_data_list)


def select_container(stats):
  # iterate over tats to create structure
  # [ { name: 'foo', cpu: 10, memory: 20}]
  container_stats = []

  for i in range(0, len(stats)):
    data = {}
    data['name'] = stats[i]['container']
    data[CPU_KEY] = replace_percentage_sign(stats[i][CPU_KEY])
    data[MEMORY_KEY] = replace_percentage_sign(stats[MEMORY_KEY]['percent'])

    container_stats.append(data)

  return selection_algorithm(container_stats)


def selection_algorithm(stats):
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

  dictionary_keys = list(diff.keys())
  sorted_diff_dict = {dictionary_keys[i]: sorted(diff.values())[i] for i in range(len(dictionary_keys))}

  ## @TODO - This should return a list instead of a sorted dictionary.
  # return sorted list of name and weights
  return sorted_diff_dict


def write_results(results):
  print(results);


def replace_percentage_sign(value):
  return value.replace('%', '')


def main():
  node_stats = retrieve_node_stats();
  selected_node_name = select_node(node_stats)[0]['name']
  selected_container = select_container(node_stats[selected_node_name]['containers'])

  write_results([])


# -------------------------------------------------------------------------------
#
# node_containers_stats = {}
# for node_name in nodes:
#   node_containers_stats_list = []
#   if (len(node_cont_stats[node_name]) != 0):
#     for i in range(len(node_cont_stats[node_name])):
#       l = {}
#       l['name'] = node_cont_stats[node_name][i]['container']
#       l[CPU_KEY] = node_cont_stats[node_name][i][CPU_KEY]
#       l[MEMORY_KEY] = node_cont_stats[node_name][i][MEMORY_KEY]['percent']
#       node_containers_stats_list.append(l)
#
#   # Dict with key =  node_name and value = list of containers with corresponding stats
#   node_containers_stats[node_name] = node_containers_stats_list
#
# print(node_containers_stats)
# sorted_node_list = selection_algorithm(node_stats)
#
# # Sorted node_list
# print(sorted_node_list)
# sorted_cont_list = {}
# for node_name in sorted_node_list:
#   sorted_cont_list[node_name] = selection_algorithm(node_containers_stats[node_name])

# Sorted container list per node
# print(sorted_cont_list)

if __name__ == "__main__":
  try:
    while True:
      main()
      time.sleep(DATA_RETRIEVAL_INTERVAL_SECONDS)
  except KeyboardInterrupt:
    print('stopped!')
