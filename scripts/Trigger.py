import os
import subprocess
import time

def watch_bucket(bucket_name):
    while True:
        # Use gsutil ls to list objects in the bucket
        result = subprocess.run(['gsutil', 'ls', 'gs://' + bucket_name], stdout=subprocess.PIPE)

        # Process the result (you can customize this based on your requirements)
        if result.returncode == 0:
            print("Bucket contents:")
            print(result.stdout.decode())
        else:
            print("Error while listing bucket contents.")

        # Sleep for a specified interval (e.g., 1 hour)
        time.sleep(3600)

if __name__ == "__main__":
    # Set your GCS bucket name here
    bucket_name = "dcase2023dataset"

    watch_bucket(bucket_name)
