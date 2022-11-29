app="workerapp"
docker build -t ${app} .
docker run -d --name mycontainer -p 8080:80 ${app}:latest

docker container ls
