# data_collection_simulation.py

import os
import shutil
import pandas as pd
from google.cloud import storage

def simulate_weekly_data_collection(csv_file_path, destination_path, segment_size=100, bucket_name="dcase2023dataset"):
    # Ensure the destination directory exists
    os.makedirs(destination_path, exist_ok=True)

    # Load the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)

    # Shuffle the DataFrame for randomness
    df = df.sample(frac=1).reset_index(drop=True)

    # Set the path to the service account key file
    key_path = "/app/newtestproject-405920-4be1a3498a32.json"

    # Create a Google Cloud Storage client with explicit credentials
    client = storage.Client.from_service_account_json(key_path)

    # Simulate weekly data collection and upload to GCS
    for i in range(0, len(df), segment_size):
        segment = df.iloc[i:i + segment_size]

        # Create a subdirectory for each week
        week_directory = os.path.join(destination_path, f'week_{i // segment_size + 1}')
        os.makedirs(week_directory, exist_ok=True)

        # Copy the selected files to the week directory
        for _, row in segment.iterrows():
            source_file_path = row['file_path']
            destination_file_path = os.path.join(week_directory, os.path.basename(source_file_path))
            shutil.copyfile(source_file_path, destination_file_path)

            # Upload the file to Google Cloud Storage
            upload_to_gcs(client, bucket_name, destination_file_path)

def upload_to_gcs(client, bucket_name, file_path):
    """Upload a file to Google Cloud Storage."""
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(os.path.basename(file_path))
    blob.upload_from_filename(file_path)

if __name__ == "__main__":
    # Replace with the actual path to your CSV file
    csv_file_path = "/app/attributes_00.csv"
    
    # Replace with the actual destination directory for simulated weekly data collection
    destination_path = "/app/data"

    # Specify the number of rows to include in each weekly segment
    segment_size = 100

    # Replace with your Google Cloud Storage bucket name
    bucket_name = "dcase2023dataset"

    # Run the simulation
    simulate_weekly_data_collection(csv_file_path, destination_path, segment_size, bucket_name)
