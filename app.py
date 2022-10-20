import requests

from flask import Flask
from .round_robin import RoundRobinLB

app = Flask(__name__)

# These are just placeholders for now
hosts = ["https://www.google.com", "https://www.cnn.com", "https://www.illinois.edu"]

loadbalancer = RoundRobinLB(hosts)

@app.route("/")
def main():

  host = loadbalancer.get_host()
  request = requests.get(host)

  return request.text
