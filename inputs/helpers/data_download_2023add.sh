#!/bin/bash

# Create directories
mkdir -p "data/dcase2023t2/eval_data/raw"

# Change to the directory
cd "data/dcase2023t2/eval_data/raw"

# Download and unzip evaluation data
machine_types=("bandsaw" "grinder" "shaker" "ToyDrone" "ToyNscale" "ToyTank" "Vacuum")

for machine_type in "${machine_types[@]}"; do
    wget "https://zenodo.org/record/7830345/files/eval_data_${machine_type}_train.zip"
    unzip "eval_data_${machine_type}_train.zip"
    rm "eval_data_${machine_type}_train.zip"  # Remove the zip file after extracting its contents
done
