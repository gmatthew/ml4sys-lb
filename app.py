import os
import json

from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def main():
  containers = get_container_stats()
  nodes = get_node_stats()
  results = {
    "containers": containers,
    "node": nodes
  }

  return jsonify(results)

def get_container_stats():
  cmd = "docker stats --no-stream --format '{\"container\": \"{{ .Container }}\", \"memory\": { \"raw\": \"{{ .MemUsage }}\", \"percent\": \"{{ .MemPerc }}\"}, \"cpu\": \"{{ .CPUPerc }}\"}'"
  stream = os.popen(cmd)
  output = stream.read()
  jsonlines = output.split('\n')

  containers = []
  for line in jsonlines[:-1]:
    data = json.loads(line)
    containers.append(data)

  return containers

def get_node_stats():
  nodes = []
  cmd = "./get_mem_stats"
  stream = os.popen(cmd)
  output = stream.read()
  jsonlines = output.split(',')
  nodes.append(jsonlines)

  cmd = "./get_cpu_stats"
  stream = os.popen(cmd)
  output = stream.read()
  jsonlines = output.split(',')
  nodes.append(jsonlines)

  return nodes
