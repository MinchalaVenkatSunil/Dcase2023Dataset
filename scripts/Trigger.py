import os
from google.cloud import storage

def process_file(data, context):
    """Triggered by a change to a Cloud Storage bucket."""
    bucket_name = data['bucket']
    file_name = data['name']

    print(f"Processing file: {file_name} in bucket: {bucket_name}")

    # Your logic to process the file goes here

if __name__ == '__main__':
    process_file({'bucket': 'dcase2023dataset', 'name': 'data1'}, None)
