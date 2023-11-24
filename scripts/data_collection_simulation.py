import os
from google.cloud import storage
import pandas as pd
from datetime import datetime

def simulate_weekly_data_collection():
    """
    Simulates weekly data collection and uploads CSV files to Google Cloud Storage.
    """
    print("Starting the weekly data collection and upload script...")

    # File paths for CSV files
    csv_file_path_fan = "/app/fan_attributes_00.csv"
    csv_file_path_bearing = "/app/bearing_attributes_00.csv"

    # Google Cloud Storage configuration
    bucket_name = "dcase2023bucketdataset"
    
    # Include year, month, and day in the folder structure
    current_date = datetime.now().strftime("%Y/%m/%d")
    destination_blob_name_fan = f"data/{current_date}/fan_attributes_00.csv"
    destination_blob_name_bearing = f"data/{current_date}/bearing_attributes_00.csv"
    
    key_path = "/app/mldocker-4713e7f8b358.json"

    # Initialize Google Cloud Storage client
    client = storage.Client.from_service_account_json(key_path)
    bucket = client.get_bucket(bucket_name)

    # Upload CSV files to Google Cloud Storage
    print(f"Uploading fan data to Google Cloud Storage: {destination_blob_name_fan}")
    blob_fan = bucket.blob(destination_blob_name_fan)
    blob_fan.upload_from_filename(csv_file_path_fan)

    print(f"Uploading bearing data to Google Cloud Storage: {destination_blob_name_bearing}")
    blob_bearing = bucket.blob(destination_blob_name_bearing)
    blob_bearing.upload_from_filename(csv_file_path_bearing)

    # Local file processing with pandas
    print("Reading CSV files with pandas...")
    fan_data = pd.read_csv(csv_file_path_fan)
    bearing_data = pd.read_csv(csv_file_path_bearing)

    # Output path for saving processed data locally
    output_path = f'/app/weekly/upload/{current_date}/'
    os.makedirs(output_path, exist_ok=True)

    # Save the processed data locally for weekly upload
    print(f"Saving fan data locally: {output_path}fan_data.csv")
    fan_data.to_csv(os.path.join(output_path, 'fan_data.csv'), index=False)
    
    print(f"Saving bearing data locally: {output_path}bearing_data.csv")
    bearing_data.to_csv(os.path.join(output_path, 'bearing_data.csv'), index=False)

    print("Weekly data collection and upload script completed.")

if __name__ == "__main__":
    print("Main started...")
    # Run the weekly data collection and upload script
    simulate_weekly_data_collection()
