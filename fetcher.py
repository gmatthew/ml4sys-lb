import json, requests

nodes = {
  "localhost": "127.0.0.1"
}

def calculate_right_container(stats):

  for node_name in stats:
    node_stats = stats[node_name]
    container_stats = node_stats["containers"]
    node_stats = node_stats["node"]

    print(container_stats)
    print(node_stats)

def main():

  node_stats = {};
  for node_name in nodes:
    ip_address = nodes[node_name]
    r = requests.get('http://'+ip_address+':5000')
    stats = json.loads(r.text)

    node_stats[node_name] = stats

  calculate_right_container(node_stats)

if __name__ == "__main__":
  main()

