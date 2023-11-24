import os
from google.cloud import storage

def upload_csv_to_gcs(csv_file_path, bucket_name, destination_blob_name, key_path):
    # Create a Google Cloud Storage client with explicit credentials
    client = storage.Client.from_service_account_json(key_path)

    # Upload the CSV file to Google Cloud Storage
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(csv_file_path)

if __name__ == "__main__":
    # Replace with the actual path to your CSV file within the Docker image
    csv_file_path = "/app/attributes_00.csv"

    # Replace with your Google Cloud Storage bucket name
    bucket_name = "dcase2023bucketdataset"

    # Replace with the desired destination blob name in GCS
    destination_blob_name = "data/attributes_00.csv"

    # Replace with the actual path to your service account key file
    key_path = "/app/mldocker-4713e7f8b358.json"

    # Run the upload script
    upload_csv_to_gcs(csv_file_path, bucket_name, destination_blob_name, key_path)
