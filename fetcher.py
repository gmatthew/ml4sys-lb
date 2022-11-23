import json, requests
import time

# Replace with worker node IPs
nodes = {
  "node1": "10.0.60.93",
  "node2": "10.0.60.194"
}

def calculate_right_container(stats):

  for node_name in stats:
    node_stats = stats[node_name]
    container_stats = node_stats["containers"]
    node_stats = node_stats["node"]

    print(container_stats)
    print(node_stats)

def main():

  #node_stats = {};
  node_cpu_stats = {};
  node_mem_stats = {};
  node_cont_stats = {};
  for node_name in nodes:
    ip_address = nodes[node_name]
    r = requests.get('http://'+ip_address+':5000')
    stats = json.loads(r.text)
    node_cpu_stats[node_name] = stats['node'][0]['cpu']
    node_mem_stats[node_name] = stats['node'][0]['memory']['percent']
    node_cont_stats[node_name] = stats['containers']
    #node_stats[node_name] = stats
  print(node_cpu_stats)
  print(node_mem_stats)
  print(node_cont_stats)

  per_cont_mem = {};
  per_cont_cpu = {};
  for node_name in nodes:
    if (len(node_cont_stats[node_name]) != 0):
      for i in range(len(node_cont_stats[node_name])):
        # Needs to be changed to store the values in a nested dictionary
        per_cont_cpu[node_name] = node_cont_stats[node_name][i]['cpu'] 
        per_cont_mem[node_name] = node_cont_stats[node_name][i]['memory']['percent']
    else:
      per_cont_cpu[node_name] = {}
      per_cont_mem[node_name] = {}
  print(per_cont_cpu)
  print(per_cont_mem)
  #print(node_stats['node1'])
  #calculate_right_container(node_stats)

if __name__ == "__main__":
  try:
    while True:
        main()
        time.sleep(5)
  except KeyboardInterrupt:
    print('stopped!')

