# import os
# from google.cloud import storage
# from datetime import datetime

# def upload_data_to_gcs(bucket_name, source_folder, key_path):
#     """Upload data to Google Cloud Storage."""
#     print("=== Starting upload_data_to_gcs ===")

#     print(f"Current working directory: {os.getcwd()}")
#     print(f"Current working directory: {os.path.pardir}")

#     client = storage.Client.from_service_account_json(key_path)
#     bucket = client.get_bucket(bucket_name)

#     # Include year, month, and day in the folder structure
#     #current_date = datetime.now().strftime("%Y/%m/%d")
#     destination_folder = f'/data/weekly/upload/'
#     # destination_folder = f'data/{current_date}/weekly_upload/'

#     print(f"Does the folder exist: {source_folder}")

#     # List all files in the source folder
#     if os.path.exists(source_folder):
#         files = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]

#         # Upload each file to Google Cloud Storage
#         for file_name in files:
#             source_file_path = os.path.join(source_folder, file_name)
#             destination_blob_name = os.path.join(destination_folder, file_name)
#             blob = bucket.blob(destination_blob_name)
#             blob.upload_from_filename(source_file_path)
#             print(f"Uploaded {file_name} to Google Cloud Storage at {destination_blob_name}")

#     else:
#         print(f"The directory '{source_folder}' does not exist.")

#     print("=== Finished upload_data_to_gcs ===")

# def main():
#     print("=== Starting main ===")

#     # Google Cloud Storage configuration
#     bucket_name = os.environ.get("GCS_BUCKET_NAME", "dcase2023bucketdataset")
#     key_path = os.environ.get("GCS_KEY_PATH", "/app/mldocker-4713e7f8b358.json")

#     # Source folder containing the data to be uploaded
#     source_folder = 'data/weekly/upload'

#     # Upload data to Google Cloud Storage
#     upload_data_to_gcs(bucket_name, source_folder, key_path)

#     print("=== Finished main ===")

# if __name__ == "__main__":
#     main()

import os
from google.cloud import storage

def upload_to_gcs(local_file_path, bucket_name, destination_blob_name, key_path):
    """Upload a file to Google Cloud Storage."""
    client = storage.Client.from_service_account_json(key_path)
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(local_file_path)
    print(f"Uploaded: {local_file_path} to {destination_blob_name}")

def transfer_data_to_gcs(local_data_folder, bucket_name, key_path):
    """Transfer locally collected data to Google Cloud Storage."""
    print("---------------------------------------------------")
    print(f"Current Working Directory: {os.getcwd()}")
    print(f"Script Directory: {os.path.dirname(os.path.realpath(__file__))}")
    print(f"Starting data transfer from {local_data_folder} to {bucket_name}...")

    for root, dirs, files in os.walk(local_data_folder):
        for file in files:
            local_file_path = os.path.join(root, file)
            destination_blob_name = os.path.relpath(local_file_path, local_data_folder)
            
            print(f"\nProcessing: {local_file_path}")
            upload_to_gcs(local_file_path, bucket_name, destination_blob_name, key_path)

    print("Data transfer completed.")
    print("---------------------------------------------------")

if __name__ == "__main__":
    print("---------------------------------------------------")
    print("Starting main...")
    
    # Set configuration details
    local_data_folder = "/app/weekly/upload/"  # Adjust to the actual local data folder
    bucket_name = os.environ.get("GCS_BUCKET_NAME", "dcase2023bucketdataset")
    key_path = os.environ.get("GCS_KEY_PATH", "/app/mldocker-4713e7f8b358.json")

    # Transfer data to Google Cloud Storage
    transfer_data_to_gcs(local_data_folder, bucket_name, key_path)
    
    print("Main completed.")
    print("---------------------------------------------------")

