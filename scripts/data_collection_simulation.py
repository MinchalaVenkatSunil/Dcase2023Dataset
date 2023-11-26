from google.cloud import storage
import os
import random
from datetime import datetime, timedelta

def download_file(bucket_name, source_blob_name, destination_file_name):
    """Downloads a file from Google Cloud Storage."""
    # json_key_path = "C:/Users/harit/Documents/Visual Studio 2022/MLDockerTest/Dcase2023Dataset/mldocker-4713e7f8b358.json"
    json_key_path = "/app/mldocker-4713e7f8b358.json"
    storage_client = storage.Client.from_service_account_json(json_key_path)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)

def list_files(bucket_name, prefix):
    """Lists all files in a GCS bucket with the given prefix."""
    json_key_path = "/app/mldocker-4713e7f8b358.json"
    storage_client = storage.Client.from_service_account_json(json_key_path)
    blobs = storage_client.list_blobs(bucket_name, prefix=prefix)
    file_names = [blob.name for blob in blobs]
    # print(f"File names in {prefix}: {file_names}")
    return file_names

def simulate_weekly_data_collection(bucket_name, dataset_folder, output_path):
    print("Starting weekly data collection simulation...")

    # Ensure the output directory exists
    os.makedirs(output_path, exist_ok=True)

    # List all machine types in the dataset
    machine_types = list_files(bucket_name, f"{dataset_folder}/")
    machine_types = list(set(machine_types))

    print(f"machine types: {(machine_types.count)}")
    machine_types = [machine_type.split('/')[1] for machine_type in machine_types if '/' in machine_type]
    machine_types = list(set(machine_types))

    print(f"machine types with split: {machine_types}")

    # Simulate weekly data collection for each machine type
    for machine_type in machine_types:
        machine_type_prefix = f"{dataset_folder}/{machine_type}"

        print(f"machine type prefix: {machine_type_prefix}")

        # List all sections for the machine type
        sections = list_files(bucket_name, f"{machine_type_prefix}/")
        sections = list(set(sections))
        sections = [section.split('/')[2] for section in sections if '/' in section]
        sections = list(set(sections))

        for section in sections:
            section_prefix = f"{machine_type_prefix}/{section}"

            # List all files in the section
            files = list_files(bucket_name, f"{section_prefix}/")
            files = list(set(files))
            files = [file.split('/')[-1] for file in files if '/' in file and file.endswith('.wav')]
            files = list(set(files))

            # Simulate weekly data collection by randomly selecting a subset of files
            random.shuffle(files)
            weekly_subset = files[:2]  # Adjust the number based on your simulation requirements

            # Download and copy the selected files to the output directory
            for file_name in weekly_subset:
                source_blob_name = f"{section_prefix}/{file_name}"
                destination_path = os.path.join(output_path, f'{machine_type}_{section}_{file_name}')

                # print(f"Downloading file: {source_blob_name} -> {destination_path}")
                download_file(bucket_name, source_blob_name, destination_path)

    print("Weekly data collection simulation completed.")

if __name__ == "__main__":
    # Set the GCS bucket name and dataset folder
    gcs_bucket_name = "dcase2023bucketdataset"
    gcs_dataset_folder = "DcaseDevDataSet"

    # Set the local output directory
    output_path = "/app/data/result/weekly/data_collection"

    simulate_weekly_data_collection(gcs_bucket_name, gcs_dataset_folder, output_path)
