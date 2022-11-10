import os
import json

from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def main():
  containers = get_container_stats()

  results = {
    "containers": containers,
    "node": {}
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
