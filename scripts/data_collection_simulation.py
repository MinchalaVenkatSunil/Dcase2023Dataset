import os
import shutil
import random
from datetime import datetime, timedelta

def simulate_weekly_data_collection(dataset_path, output_path):
    print("=== Starting Weekly Data Collection Simulation ===")

    # Ensure the output directory exists
    os.makedirs(output_path, exist_ok=True)

    # List all machine types in the dataset
    machine_types = [dir_name for dir_name in os.listdir(dataset_path) if os.path.isdir(os.path.join(dataset_path, dir_name))]
    
    print(f"Machine Types: {machine_types}")

    # Simulate weekly data collection for each machine type
    for machine_type in machine_types:
        machine_type_path = os.path.join(dataset_path, machine_type)

        # List all sections for the machine type
        sections = [dir_name for dir_name in os.listdir(machine_type_path) if os.path.isdir(os.path.join(machine_type_path, dir_name))]

        print(f"Processing Machine Type: {machine_type}")

        for section in sections:
            section_path = os.path.join(machine_type_path, section)

            # List all files in the section
            files = [file_name for file_name in os.listdir(section_path) if file_name.endswith('.wav')]

            print(f"Processing Section: {section}")

            # Simulate weekly data collection by randomly selecting a subset of files
            random.shuffle(files)
            weekly_subset = files[:10]  # Adjust the number based on your simulation requirements

            # Copy the selected files to the output directory
            for file_name in weekly_subset:
                source_path = os.path.join(section_path, file_name)
                destination_path = os.path.join(output_path, f'{machine_type}_{section}_{file_name}')

                print(f"Copying: {source_path} to {destination_path}")
                shutil.copyfile(source_path, destination_path)

    print("=== Weekly Data Collection Simulation Completed ===")

if __name__ == "__main__":
    # Set the paths for the dataset and output directory
    dataset_path = "/inputs/dev_data"
    output_path = "/inputs/result"

    # dataset_path = "C:\Users\harit\Documents\Visual Studio 2022\MLDockerTest\Dcase2023Dataset\inputs\dev_data"
    # output_path = "C:\Users\harit\Documents\Visual Studio 2022\MLDockerTest\Dcase2023Dataset\inputs\result"

    simulate_weekly_data_collection(dataset_path, output_path)
