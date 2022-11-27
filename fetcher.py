import json, requests
import time

# Replace with worker node IPs
NODES = {
  "node1": "172.31.14.180",
  "node2": "172.31.0.251"
}

CPU_KEY = 'cpu'
MEMORY_KEY = 'memory'
NAME_KEY = 'name'
PERCENTAGE_KEY = 'percentage'

DATA_RETRIEVAL_INTERVAL_SECONDS = 5

#retrieves data from the collectors
def retrieve_stats():
  collected_stats = {}

  for node_name in NODES:
    ip_address = NODES[node_name]
    r = requests.get('http://' + ip_address + ':5000')
    stats = json.loads(r.text)

    collected_stats[node_name] = stats

  return collected_stats


#returns the list of nodes
def select_node(collected_stats):
  node_data_list = []

  for node_name in collected_stats:
    stats = collected_stats[node_name]
    node = stats['node'][0]

    data = {}
    data['name'] = node_name
    data[CPU_KEY] = replace_percentage_sign(node[CPU_KEY])
    data[MEMORY_KEY] = replace_percentage_sign(node[MEMORY_KEY]['percent'])

    node_data_list.append(data)

  return selection_algorithm(node_data_list)


#returns the list of containers running in the first choice node 
def select_container(stats):
  container_stats = []

  for i in range(0, len(stats)):
    data = {}
    data['name'] = stats[i]['container']
    data[CPU_KEY] = replace_percentage_sign(stats[i][CPU_KEY])
    data[MEMORY_KEY] = replace_percentage_sign(stats[i][MEMORY_KEY]['percent'])

    container_stats.append(data)

  return selection_algorithm(container_stats)

#returns the top choice of stats list (container or node)
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
  sorted_list = list(sorted_diff_dict.keys())

  ## @TODO - This should return a list instead of a sorted dictionary.
  # Returns the top choice or value at index 0
  return sorted_list[0]


#writes first choice node and container name to results file
def write_results(node_name, container_name):
  f = open("result.txt", "w")
  f.write("node: " + node_name)
  f.write("\ncontainer: " + container_name)
  f.close()


def replace_percentage_sign(value):
  return value.replace('%', '')


def main():
  collected_stats = retrieve_stats();
  selected_node = select_node(collected_stats)
  selected_container = select_container(collected_stats[selected_node]['containers'])
  write_results(selected_node, selected_container)


if __name__ == "__main__":
  try:
    while True:
      main()
      time.sleep(DATA_RETRIEVAL_INTERVAL_SECONDS)
  except KeyboardInterrupt:
    print('stopped!')
