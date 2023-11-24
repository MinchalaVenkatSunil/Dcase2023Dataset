import os
from google.cloud import storage
import pandas as pd
from datetime import datetime

# def simulate_weekly_data_collection_other_solution():
#     """
#     Simulates weekly data collection and uploads CSV files to Google Cloud Storage.
#     """
#     # File paths for CSV files
#     csv_file_path_fan = "/app/fan_attributes_00.csv"
#     csv_file_path_bearing = "/app/bearing_attributes_00.csv"

#     # Google Cloud Storage configuration
#     bucket_name = "dcase2023bucketdataset"
    
#     # Include year, month, and day in the folder structure
#     current_date = datetime.now().strftime("%Y/%m/%d")
#     destination_blob_name_fan = f"data/{current_date}/fan_attributes_00.csv"
#     destination_blob_name_bearing = f"data/{current_date}/bearing_attributes_00.csv"
    
#     key_path = "/app/mldocker-4713e7f8b358.json"

#     # Initialize Google Cloud Storage client
#     client = storage.Client.from_service_account_json(key_path)
#     bucket = client.get_bucket(bucket_name)

#     # Upload CSV files to Google Cloud Storage
#     blob_fan = bucket.blob(destination_blob_name_fan)
#     blob_fan.upload_from_filename(csv_file_path_fan)

#     blob_bearing = bucket.blob(destination_blob_name_bearing)
#     blob_bearing.upload_from_filename(csv_file_path_bearing)

#     """
#     Simulates weekly data collection and uploads CSV files to local OS.
#     """
#     # Local file processing with pandas
#     fan_data = pd.read_csv(csv_file_path_fan)
#     bearing_data = pd.read_csv(csv_file_path_bearing)

#     # Output path for saving processed data locally
#     output_path = f'/app/weekly/upload/{current_date}/'
#     os.makedirs(output_path, exist_ok=True)

#     # Save the processed data locally for weekly upload
#     fan_data.to_csv(os.path.join(output_path, 'fan_data.csv'), index=False)
#     bearing_data.to_csv(os.path.join(output_path, 'bearing_data.csv'), index=False)

def download_data_from_gcs(bucket_name, source_blob_name, destination_file_path, key_path):
    """Download a file from Google Cloud Storage."""
    client = storage.Client.from_service_account_json(key_path)
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_path)

def simulate_weekly_data_collection():
    """
    Assuming the source data will be available weekly under the secured GCP bucket "dcase2023bucketdataset".
    Simulates weekly data collection and downloads CSV files from Google Cloud Storage.
    """
    print("Starting the weekly data collection and download script...")

    # Google Cloud Storage configuration
    # bucket_name = "dcase2023bucketdataset"
    # key_path = "/app/mldocker-4713e7f8b358.json"

    # Google Cloud Storage configuration
    bucket_name = os.environ.get("GCS_BUCKET_NAME", "")
    key_path = os.environ.get("GCS_KEY_PATH", "")

    # Include year, month, and day in the folder structure
    current_date = datetime.now().strftime("%Y/%m/%d")
    destination_folder = f'/app/weekly/upload/{current_date}/'
    os.makedirs(destination_folder, exist_ok=True)

    # List of machinery types
    machinery_types = ["fan", "bearing", "gearbox", "slider", "ToyCar", "ToyTrain", "valve"]

    # Download CSV files for each machinery type
    for machinery_type in machinery_types:
        source_blob_name = f"DcaseDevDataSet/{machinery_type}/attributes_00.csv"
        destination_file_path = os.path.join(destination_folder, f'{machinery_type}_attributes_00.csv')
        download_data_from_gcs(bucket_name, source_blob_name, destination_file_path, key_path)
        print(f"Downloaded {machinery_type} data from Google Cloud Storage to {destination_file_path}")

    print("Weekly data collection and download script completed.")

if __name__ == "__main__":
    simulate_weekly_data_collection()
