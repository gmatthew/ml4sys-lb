#!/bin/bash

# This script is used to run the application

cd ml-lb/ && python3 run_experiments.py --num_workers 10 --service_rates 0.15 0.25 0.35 0.45 0.55 0.65 0.75 0.85 0.95 1.05 --result_folder ./trained_results/10_value_networks/ --model_folder ./trained_results/parameters/10_value_networks/