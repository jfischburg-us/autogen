import csv
from datetime import datetime
import json
import requests
import time

from azure.storage.blob import BlobServiceClient


# Azure Setup
CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=caito;AccountKey=o0Qzvj9Z4hWJ0uJwAPMjEEPJt3H6/9LGvm7bwCQKKC1ripO/eLtRQthDTmCbOa+lyFDaLPt4MNKv+AStbNvzPQ==;EndpointSuffix=core.windows.net"
ACCOUNT_NAME = "caito"
CONTAINER_NAME = "caito"

# Cognitive/Speech Services Configuration
SPEECH_KEY = "3f80ab84124d4539aeef2610dab29da0"
SERVICE_REGION = "eastus2"


def create_transcription_job(name, language, content_urls):
    """
    Create a batch transcription job and poll the API until the job is complete.

    Parameters:
    name (str): The name of the transcription job.
    language (str): The language of the audio data.
    content_urls (list[str]): The URLs of the audio files in Azure Blob Storage.

    Returns:
    dict: The final response from the API when the job is complete.
    """
    # Set up the API endpoint
    endpoint = (
        "https://eastus2.api.cognitive.microsoft.com/speechtotext/v3.1/transcriptions"
    )

    # Set up the headers
    headers = {
        "Ocp-Apim-Subscription-Key": SPEECH_KEY,
        "Content-Type": "application/json",
    }

    # Set up the body
    body = {
        "contentUrls": content_urls,
        "properties": {
            "wordLevelTimestampsEnabled": True,
            "punctuationMode": "DictatedAndAutomatic",
            "profanityFilterMode": "Masked",
        },
        "locale": language,
        "displayName": name,
    }

    # Make the POST request to create the transcription job
    response = requests.post(endpoint, headers=headers, data=json.dumps(body))
    response.raise_for_status()  # Raise an exception if the request failed

    # Get the URL of the created transcription job
    transcription_url = response.json()["self"]

    while True:
        # Make a GET request to check the status of the transcription job
        response = requests.get(transcription_url, headers=headers)
        response.raise_for_status()  # Raise an exception if the request failed

        status = response.json()["status"]
        print(f"{datetime.now()} Current status: {status}")

        if status in {"Succeeded", "Failed"}:
            # If the job is complete, return the final response
            return response.json()
        else:
            # If the job is not yet complete, wait for a while before checking again
            time.sleep(30)


def upload_file_to_blob(blob_service_client, container_name, blob_name, file_path):
    """
    Upload a file to Azure Blob Storage.

    Parameters:
    blob_service_client (BlobServiceClient): The BlobServiceClient object.
    container_name (str): The name of the container.
    blob_name (str): The name of the blob.
    file_path (str): The local path of the file.

    Returns:
    None
    """
    blob_client = blob_service_client.get_blob_client(container_name, blob_name)
  
    with open(file_path, "rb") as f:
        blob_client.upload_blob(f, overwrite=True)


def main():
    """
    Main function to read a CSV file, create a batch transcription job for each audio file,
    and print out the results.

    Returns:
    None
    """

    # Create a BlobServiceClient object
    blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)

    with open("videos.txt") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            title = row["Title"]
            video_url = row["URL"]

            # Create a batch transcription job for each audio file
            content_url = f"https://{ACCOUNT_NAME}.blob.core.windows.net/{CONTAINER_NAME}/audio/{title}.wav"
            print(f"Creating batch transcription job for {title}")
            response = create_transcription_job(title, "en-US", [content_url])

            headers = {
                "Ocp-Apim-Subscription-Key": SPEECH_KEY,
                "Content-Type": "application/json",
            }

            files = requests.get(response["links"]["files"], headers=headers).json()  

            print(files)
            
            # Access the 'values' key of the 'files' dictionary to get the list of files
            for file in files['values']:
                file_url = file["links"]["contentUrl"]
                file_response = requests.get(file_url, headers=headers)
                file_response.raise_for_status()

                # Write the file content to a local file
                file_path = f"{title}.txt"
                with open(file_path, "wb") as f:
                    f.write(file_response.content)

                # Upload the local file to Azure Blob Storage
                blob_name = f"transcripts/{title}.txt"
                upload_file_to_blob(
                    blob_service_client, CONTAINER_NAME, blob_name, file_path
                )

            print(f"Results for {title}:")
            print(json.dumps(response, indent=4))


if __name__ == "__main__":
    """
    Entry point of the script.
    """
    main()
