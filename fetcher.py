import json, requests
import time

# Replace with worker node IPs
nodes = {
  "node1": "10.0.60.93",
  "node2": "10.0.60.194"
}

def select_node(node_stats):
  return selection_algorithm(node_stats)  

def select_container(stats):
  # iterate over tats to create structure
  # [ { name: 'foo', cpu: 10, memory: 20}]
  container_stats = []

  return selection_algorithm(container_stats)

def selection_algorithm(stats):
  # stats argument structure => [ { name: 'foo', cpu: 10, memory: 20}]
  cpu_stats = []
  mem_stats = []
  diff = {}
  for i in range(len(stats)):
    cpu_val = stats[i]['cpu'].replace('%', '')
    cpu_stats.append(float(cpu_val))
    mem_val = stats[i]['memory'].replace('%', '')
    mem_stats.append(float(mem_val))
  
  cpu_stats.sort()
  mem_stats.sort()

  for i in range(len(stats)):
    cpu_val = stats[i]['cpu'].replace('%', '')
    mem_val = stats[i]['memory'].replace('%', '')
    diff[stats[i]['name']] = abs(float(cpu_val) - cpu_stats[0]) + abs(float(mem_val) - mem_stats[0])

  dictionary_keys = list(diff.keys())
  sorted_diff_dict = {dictionary_keys[i]: sorted(diff.values())[i] for i in range(len(dictionary_keys))}

  #return sorted list of name and weights
  return sorted_diff_dict


def write_results(results):
  print(results);

def main():

  # make call to nodes api
  # aggregate stats by nodes
  # call select nodes with node stats
  # call select container with containter stats of selected nodes
  # write the order list of containers to file

  node_stats = []
  cont_stats = []
  node_cont_stats = {}
  for node_name in nodes:
    ip_address = nodes[node_name]
    r = requests.get('http://'+ip_address+':5000')
    stats = json.loads(r.text)
    d = {}
    d['name'] = node_name
    d['cpu'] = stats['node'][0]['cpu']
    d['memory'] = stats['node'][0]['memory']['percent']

    #List of nodes and corresponding stats
    node_stats.append(d)
    node_cont_stats[node_name] = stats['containers']
  print(node_stats)

  node_containers_stats = {}
  for node_name in nodes:
    node_containers_stats_list = []
    if (len(node_cont_stats[node_name]) != 0):
      for i in range(len(node_cont_stats[node_name])):
        l = {}
        l['name'] = node_cont_stats[node_name][i]['container']
        l['cpu'] = node_cont_stats[node_name][i]['cpu']
        l['memory'] = node_cont_stats[node_name][i]['memory']['percent']
        node_containers_stats_list.append(l)

    # Dict with key =  node_name and value = list of containers with corresponding stats
    node_containers_stats[node_name] = node_containers_stats_list

  print(node_containers_stats)
  sorted_node_list = selection_algorithm(node_stats)
  
  # Sorted node_list
  print(sorted_node_list)
  sorted_cont_list = {}
  for node_name in sorted_node_list:
    sorted_cont_list[node_name] = selection_algorithm(node_containers_stats[node_name])

  #Sorted container list per node
  print(sorted_cont_list)

if __name__ == "__main__":
  try:
    while True:
        main()
        time.sleep(5)
  except KeyboardInterrupt:
    print('stopped!')