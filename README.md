# Machine Learning For Systems
### Load Balancer Application

## Installation

To run the training and experiments, satisfy the requirements with
```bash
$ pip install -r requirements.txt
```

## Train Model
```bash
$ ./train.sh
```

## Run Experiments
```bash
$ ./run.sh
```

If you meet `OSError: [Errno 24] Too many open files`, please use `ulimit -n ${num}` to adjust your environment.