import os
from google.cloud import storage

def upload_csv_to_gcs(
    csv_file_path_fan, 
    csv_file_path_bearing,
    bucket_name, 
    destination_blob_name_fan, 
    destination_blob_name_bearing, 
    key_path):
    
    print(f"Uploading CSV files to Google Cloud Storage...")
    
    # Create a Google Cloud Storage client with explicit credentials
    client = storage.Client.from_service_account_json(key_path)

    # Upload the CSV files to Google Cloud Storage
    bucket = client.get_bucket(bucket_name)
    
    # Upload fan attributes CSV
    blob_fan = bucket.blob(destination_blob_name_fan)
    blob_fan.upload_from_filename(csv_file_path_fan)
    print(f"Uploaded fan attributes CSV to {destination_blob_name_fan}")

    # Upload bearing attributes CSV
    blob_bearing = bucket.blob(destination_blob_name_bearing)
    blob_bearing.upload_from_filename(csv_file_path_bearing)
    print(f"Uploaded bearing attributes CSV to {destination_blob_name_bearing}")

if __name__ == "__main__":

    print(" STARTING 1...")

    # Replace with the actual path to your CSV files within the Docker image
    csv_file_path_fan = "/app/fan_attributes_00.csv"
    csv_file_path_bearing = "/app/bearing_attributes_00.csv"

    print(" STARTING 2...")

    # Replace with your Google Cloud Storage bucket name
    bucket_name = "dcase2023bucketdataset"

    print(" STARTING 3...")

    # Replace with the desired destination blob names in GCS
    destination_blob_name_fan = "data/fan_attributes_00.csv"
    destination_blob_name_bearing = "data/bearing_attributes_00.csv"

    print(" STARTING 4...")

    # Replace with the actual path to your service account key file
    key_path = "/app/mldocker-4713e7f8b358.json"

    print(" STARTING 5...")

    # Run the upload script
    upload_csv_to_gcs(
        csv_file_path_fan,
        csv_file_path_bearing,
        bucket_name,
        destination_blob_name_fan,
        destination_blob_name_bearing,
        key_path
    )
