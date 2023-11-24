# data_collection_simulation.py

import os
import shutil
import pandas as pd
from google.cloud import storage

def simulate_weekly_data_collection(csv_file_path, destination_path, segment_size=100, bucket_name="dcase2023dataset"):
    os.makedirs(destination_path, exist_ok=True)

    df = pd.read_csv(csv_file_path)
    df = df.sample(frac=1).reset_index(drop=True)

    key_path = "/app/key.json"
    client = storage.Client.from_service_account_json(key_path)

    for i in range(0, len(df), segment_size):
        segment = df.iloc[i:i + segment_size]
        week_directory = os.path.join(destination_path, f'week_{i // segment_size + 1}')
        os.makedirs(week_directory, exist_ok=True)

        for _, row in segment.iterrows():
            source_file_path = row['file_path']
            destination_file_path = os.path.join(week_directory, os.path.basename(source_file_path))
            shutil.copyfile(source_file_path, destination_file_path)
            upload_to_gcs(client, bucket_name, destination_file_path)

def upload_to_gcs(client, bucket_name, file_path):
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(os.path.basename(file_path))
    blob.upload_from_filename(file_path)

if __name__ == "__main__":
    csv_file_path = "/app/fan_attributes_00.csv"
    destination_path = "/app/data"
    segment_size = 100
    bucket_name = "dcase2023dataset"
    simulate_weekly_data_collection(csv_file_path, destination_path, segment_size, bucket_name)
