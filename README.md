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
export FLASK_APP=app.py
export FLASk_ENV=development
```

## Start Server
```bash
$ flask run --host=0.0.0.0
```


## Fetcher Setup
```bash
python3 fetcher-main.py --output envoy-config/eds.yaml
```


## Containers 

### Build & Push

```bash
docker build -t gmatthew/hpn-worker-app .
docker push gmatthew/hpn-worker-app:latest
```
### Launch Containers
This will launch container on worker nodes
```bash
docker container rm container1
docker container rm container2
docker container rm container3
docker run -d --env APPNAME=container21 --name container21 --cpus=".5" --memory="512m" -p 8080:80 gmatthew/hpn-worker-app:latest
docker run -d --env APPNAME=container22 --name container22 --cpus=".5" --memory="512m" -p 8081:80 gmatthew/hpn-worker-app:latest
docker run -d --env APPNAME=container23 --name container23 --cpus=".5" --memory="512m" -p 8082:80 gmatthew/hpn-worker-app:latest
```
