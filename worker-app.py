import os
import json

from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def main():

  # orchestration
  # based on query param work type
  # e.g localhost/?worktype=cpu  or localhost/?worktype=mem

  # switch(workertype)



  # A
  # this main application running on the worker nodes

  # two methods
  # 1 - cpu intensive
  # 2 - memory intensive
  # using query parameter, we will invoke different mix of workloads (cpu and memory)


  # B
  # Dockerize this application
  # 1. create Dockerfile
  # 2. build contianer
  # 3. publish to docker hub
  # 4. deploy to worker nodes


  # C - experiment setup
  # 1. restrict the docker containers to be using the lowest memory and cpu allowed (.5 vCPU .5 Mem)
  # ->>>> ?memtype=mem   ?memtype=cpu
  # 2 . loginto application and run memtester in the container


  # Experiments
  #

  return jsonify(results)

def do_normal_work():

  return


def do_cpu_intensive_work():
  # do some metrics calculation over how many iterations

  return


def do_memory_intensive_work():
  # do some memory allocation stuff that takes up space

  return
