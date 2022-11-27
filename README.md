# Machine Learning For Systems
### Load Balancer Application

## Installation

To run the app flawlessly, satisfy the requirements
```bash
$ pip install -r requirements.txt
```

Run the following commands on the worker nodes to expose port 5000 to inbound traffic
```
sudo apt install firewalld
sudo firewall-cmd --add-port=5000/tcp --permanent
sudo firewall-cmd --reload
```

## Set Environment Variables
```bash
$ export FLASK_APP=app.py
$ export FLASk_ENV=development
```

## Start Server
```bash
$ flask run --host=0.0.0.0
```


## Fetcher Setup
```bash
python3 fetcher-main.py --output "/tmp/foo.txt"
```
