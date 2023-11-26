import os
import shutil
import random
from datetime import datetime, timedelta

from google.cloud import storage  # Install this library using: pip install google-cloud-storage

def simulate_weekly_data_collection(output_path, weekly_subset_count):
    print("=== Starting Weekly Data Collection Simulation ===")

    # Ensure the output directory exists
    os.makedirs(output_path, exist_ok=True)

    # Read the dataset path from the environment variable
    dataset_path = os.environ.get('DATASET_PATH')
    if not dataset_path:
        raise ValueError("DATASET_PATH environment variable not set.")

    # Read the dataset path from the environment variable
    gcp_key_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    if not gcp_key_path:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")

    # Initialize Google Cloud Storage client
    storage_client = storage.Client.from_service_account_json(gcp_key_path)

    # List all machine types in the dataset
    machine_types = [dir_name for dir_name in storage_client.list_blobs(dataset_path, prefix='') if '/' in dir_name.name]
    
    print(f"Machine Types: {machine_types}")

    # Simulate weekly data collection for each machine type
    for machine_type_blob in machine_types:
        machine_type_path = machine_type_blob.name

        # List all sections for the machine type
        sections = [dir_name for dir_name in storage_client.list_blobs(machine_type_path, prefix=machine_type_path) if '/' in dir_name.name]

        print(f"Processing Machine Type: {machine_type_path}")

        for section_blob in sections:
            section_path = section_blob.name

            # List all files in the 'train' subdirectory
            train_path = os.path.join(section_path, 'train')
            train_files = [blob.name for blob in storage_client.list_blobs(train_path, prefix=train_path)]

            print("Train Path:", train_path)
            print("Train Files:", train_files)

            # List all files in the 'test' subdirectory
            test_path = os.path.join(section_path, 'test')
            test_files = [blob.name for blob in storage_client.list_blobs(test_path, prefix=test_path)]

            print("Test Path:", test_path)
            print("Test Files:", test_files)

            # Combine 'train' and 'test' files for processing
            files = train_files + test_files

            print(f"Processing Section: {section_path}")
            print(f"Processing files count: {len(files)}")

            # Simulate weekly data collection by randomly selecting a subset of files
            random.shuffle(files)
            weekly_subset = files[:weekly_subset_count] 
            print(f"Weekly Subset: {weekly_subset}")

            # Copy the selected files to the output directory
            for file_name in weekly_subset:
                print(f"Copying: {file_name}")

                source_path = os.path.join(section_path, 'train' if file_name in train_files else 'test', file_name)
                destination_path = os.path.join(output_path, f'{machine_type_path}_{section_path}_{file_name}')

                print(f"Copying: {source_path} to {destination_path}")
                shutil.copyfile(source_path, destination_path)

    print("=== Weekly Data Collection Simulation Completed ===")

if __name__ == "__main__":
    # Set the output directory
    output_path = "/app/result/weekly"
    weekly_subset_count = 2

    # Read the Google Cloud Storage dataset path and credentials file path from environment variables
    os.environ['DATASET_PATH'] = "dcase2023bucketdataset/DcaseDevDataSet"
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/app/mldocker-4713e7f8b358.json"

    simulate_weekly_data_collection(output_path, weekly_subset_count)
