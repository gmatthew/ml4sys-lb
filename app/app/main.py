import os
import json
import time
import numpy as np

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def hello():
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

  return "Worker App | Root"

def multiply_matrix(A,B):
  global C
  C = np.zeros((A.shape[0],B.shape[1]),dtype = int)
  if  A.shape[1] == B.shape[0]:
      for i in range(len(A)):
          for j in range(len(B[0])):
              for k in range(len(B)):
                  C[i][j] += A[i][k] * B[k][j]
  return C

@app.route('/cpu')
def do_cpu_intensive_work():
  # do some metrics calculation over how many iterations
  np.random.seed(27)
  A = np.random.randint(1,35000,size = (250, 250))
  B = np.random.randint(1,56000,size = (250, 250))
  C = multiply_matrix(A,B)

  #return(C[0][0])
  return "Worker App | CPU"


@app.route('/memory')
def do_memory_intensive_work():
  # do some memory allocation stuff that takes up space
  d = {}
  i = 0
  for j in range(0,10):
    for i in range(0, 10000000):
      d[i] = 'A'*1024
      if i % 10000 == 0:
        c = i

  #return(c)
  return "Worker App | Memory"

## JMeter (http://foo.com/?type=cpu|memory ----> envoy ----> workers
# if __name__ == "__main__":
#   # Only for debugging while developing
#   app.run(host='0.0.0.0', debug=True, port=80)



## Tomorrow
 # load generation
 # jmeter or wrk2
