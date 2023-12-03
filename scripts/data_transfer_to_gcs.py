import logging
import os
import requests
import base64
from google.auth.transport.requests import Request
from google.auth.transport.requests import AuthorizedSession
from google.oauth2 import service_account

# Set up logging configuration
logging.basicConfig(
    filename='data_transfer_to_gcs.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def get_access_token(json_key_path):
    try:
        # Load service account key
        credentials = service_account.Credentials.from_service_account_file(
            json_key_path,
            scopes=('https://www.googleapis.com/auth/cloud-platform',),
        )

        # Obtain an access token
        credentials.refresh(Request())

        access_token = credentials.token

        logging.info(f"token: {access_token}")
        return access_token
    except Exception as e:
        logging.error(f"Error obtaining access token: {str(e)}")
        # Handle the error as needed...

def transfer_weekly_data_to_gcs(local_data_path, gcs_bucket_name, gcs_destination_folder, gcp_function_url):
    """Transfer locally collected data to Google Cloud Storage via Google Cloud Function."""
    logging.info("Venkat Starting weekly data transfer to Google Cloud Storage...")

    # Obtain access token
    json_key_path = "C:/Users/harit/Documents/Visual Studio 2022/MLDockerTest/Dcase2023Dataset/mldocker-key-gcp.json"
    access_token = get_access_token(json_key_path)

    # Set up headers for the request
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }

    try:
        # List files in the specified local data path
        local_files = [f for f in os.listdir(local_data_path) if os.path.isfile(os.path.join(local_data_path, f))]

        for local_file in local_files:
            local_file_path = os.path.join(local_data_path, local_file)

            # Read content of the file
            with open(local_file_path, 'rb') as file:
                content = file.read()

            # Base64 encode the content if it's bytes
            if isinstance(content, bytes):
                content = base64.b64encode(content).decode('utf-8')

            # Skip the file if content is None
            if content is None:
                logging.warning(f"Skipping file {local_file} because content is None.")
                continue

            # Prepare data payload for the Google Cloud Function
            data = {
                'file_name': local_file,
                'content': content
            }

            try:
                # Send data to Google Cloud Function
                response = requests.post(gcp_function_url + "/process_data", json=data, headers=headers)

                # Check the response status code
                if response.status_code == 401:
                    logging.error("Unauthorized request. Check your authorization credentials.")
                else:
                    logging.info(f"Successfully transferred data: {data.get('file_name')}, Response: {response.text}")
                    
            except Exception as e:
                logging.error(f"Failed to transfer data: {data.get('file_name')}, Error: {str(e)}")

        logging.info("Weekly data transfer to Google Cloud Storage completed.")
    except Exception as e:
        logging.error(f"Error during data transfer: {str(e)}")

if __name__ == "__main__":
    local_data_path = "C:/Users/harit/Documents/temp/result/result/result/result"
    gcs_bucket_name = "dcase2023bucketdataset"
    gcs_destination_folder = "DcaseDevDataSetResult"
    gcp_function_url = "https://europe-north1-mldocker.cloudfunctions.net/process_data"

    transfer_weekly_data_to_gcs(local_data_path, gcs_bucket_name, gcs_destination_folder, gcp_function_url)
