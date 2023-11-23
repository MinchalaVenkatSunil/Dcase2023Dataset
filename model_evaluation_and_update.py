import os
from google.cloud import storage
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

def download_data_from_gcs(bucket_name, data_directory):
    # Set your Google Cloud Storage credentials
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/your/keyfile.json"

    # Create a storage client
    storage_client = storage.Client()

    # Get the bucket
    bucket = storage_client.get_bucket(bucket_name)

    # List all files in the bucket
    blobs = bucket.list_blobs()

    # Download files to the specified data directory
    for blob in blobs:
        destination_file = os.path.join(data_directory, blob.name)
        blob.download_to_filename(destination_file)
        print(f"File {blob.name} downloaded to {destination_file}")

def train_model(data_directory, model_output_path):
    # Load and preprocess your training data
    # Example: Replace this with your actual data loading and preprocessing code
    # X, y = load_and_preprocess_data(data_directory)

    # For illustration purposes, use a simple RandomForestClassifier
    model = RandomForestClassifier()

    # Split the data into training and validation sets
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model
    model.fit(X_train, y_train)

    # Evaluate the model (add your evaluation code here)

    # Save the trained model
    joblib.dump(model, model_output_path)
    print(f"Model saved to {model_output_path}")

if __name__ == "__main__":
    # Replace these values with your actual GCS bucket name, data directory, and model output path
    gcs_bucket_name = "your-gcs-bucket-name"
    data_directory = "/path/to/your/data/directory"
    model_output_path = "/path/to/your/output/model.joblib"

    # Download training data from GCS
    download_data_from_gcs(gcs_bucket_name, data_directory)

    # Train the model
    train_model(data_directory, model_output_path)

