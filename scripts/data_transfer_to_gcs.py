import os
from google.cloud import storage
from datetime import datetime

def upload_data_to_gcs(bucket_name, source_folder, key_path):
    """Upload data to Google Cloud Storage."""
    client = storage.Client.from_service_account_json(key_path)
    bucket = client.get_bucket(bucket_name)

    # Include year, month, and day in the folder structure
    current_date = datetime.now().strftime("%Y/%m/%d")
    destination_folder = f'data/{current_date}/weekly_upload/'

    # List all files in the source folder
    if os.path.exists(source_folder):
        files = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]

        # Upload each file to Google Cloud Storage
        for file_name in files:
            source_file_path = os.path.join(source_folder, file_name)
            destination_blob_name = os.path.join(destination_folder, file_name)
            blob = bucket.blob(destination_blob_name)
            blob.upload_from_filename(source_file_path)
            print(f"Uploaded {file_name} to Google Cloud Storage at {destination_blob_name}")
    else:
        print(f"The directory '{source_folder}' does not exist.")

def main():
    # Google Cloud Storage configuration
    bucket_name = os.environ.get("GCS_BUCKET_NAME", "dcase2023dataset")
    key_path = os.environ.get("GCS_KEY_PATH", "/app/newtestproject-405920-4be1a3498a32.json")

    # Source folder containing the data to be uploaded
    source_folder = '/data'

    # Upload data to Google Cloud Storage
    upload_data_to_gcs(bucket_name, source_folder, key_path)

if __name__ == "__main__":
    main()
