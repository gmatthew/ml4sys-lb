import os
import json

from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def main():
  containers = get_container_stats()
  node = get_node_stats()
  results = {
    "node": node,
    "containers": containers
  }

  return jsonify(results)

def get_container_stats():
  cmd = "docker stats --no-stream --format '{\"container\": \"{{ .Name }}\", \"memory\": { \"raw\": \"{{ .MemUsage }}\", \"percent\": \"{{ .MemPerc }}\"}, \"cpu\": \"{{ .CPUPerc }}\"}'"
  stream = os.popen(cmd)
  output = stream.read()
  jsonlines = output.split('\n')

  containers = []
  for line in jsonlines[:-1]:
    data = json.loads(line)
    containers.append(data)

  return containers

def get_node_stats():
  node = []
  cmd = "./get_mem_stats"
  stream = os.popen(cmd)
  output1 = stream.read()
  cmd = "./get_cpu_stats"
  stream = os.popen(cmd)
  output2 = stream.read()
  output = output1 + ", " + output2
  node.append(json.loads(output))
  return node
