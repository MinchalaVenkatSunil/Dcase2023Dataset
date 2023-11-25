#!/bin/bash

# Create directory
mkdir -p "data/dcase2023t2/dev_data/raw"

# Download dev data
cd "data/dcase2023t2/dev_data/raw"

# List of machine types
machine_types=("bearing" "fan" "gearbox" "slider" "ToyCar" "ToyTrain" "valve")

# Loop through machine types
for machine_type in "${machine_types[@]}"; do
    # Download zip file
    wget "https://zenodo.org/record/7882613/files/dev_${machine_type}.zip"

    # Unzip the file
    unzip "dev_${machine_type}.zip"

    # Optional: Remove the zip file if you want to save space
    rm "dev_${machine_type}.zip"
done
