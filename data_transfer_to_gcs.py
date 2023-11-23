import os
from google.cloud import storage
import json

def upload_to_gcs(data_directory, bucket_name):
    # Set your Google Cloud Storage credentials
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/your/keyfile.json"

    # Create a storage client
    storage_client = storage.Client()

    # Get the bucket
    bucket = storage_client.get_bucket(bucket_name)

    # Iterate over files in the data directory
    for filename in os.listdir(data_directory):
        if filename.endswith(".json"):
            file_path = os.path.join(data_directory, filename)

            # Read metadata from the JSON file
            with open(file_path, "r") as f:
                metadata = json.load(f)

            # Upload the file to GCS with metadata
            blob = bucket.blob(filename)
            blob.upload_from_filename(file_path, content_type="application/json", metadata=metadata)

            print(f"File {filename} uploaded to GCS with metadata: {metadata}")

if __name__ == "__main__":
    # Replace these values with your actual data directory and GCS bucket name
    data_directory = "/path/to/your/data/directory"
    bucket_name = "your-gcs-bucket-name"

    upload_to_gcs(data_directory, bucket_name)
