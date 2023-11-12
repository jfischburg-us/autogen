# Standard Imports
import csv
import json
import os
import requests
import string
import time

# Video Imports
from pydub import AudioSegment
from pytube import YouTube

# Azure Imports
from azure.cognitiveservices.speech import SpeechConfig, AudioConfig, SpeechRecognizer
from azure.storage.blob import BlobServiceClient


# Azure Setup
CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=caito;AccountKey=o0Qzvj9Z4hWJ0uJwAPMjEEPJt3H6/9LGvm7bwCQKKC1ripO/eLtRQthDTmCbOa+lyFDaLPt4MNKv+AStbNvzPQ==;EndpointSuffix=core.windows.net"
ACCOUNT_NAME = "caito"
CONTAINER_NAME = "caito"
blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)

<<<<<<< HEAD
# Cognitive/Speech Services Setup
SPEECH_KEY = "e6def55c6d904eefa7afe1efa63ac84f"
SERVICE_REGION = "eastus2"
=======
# Cognitive/Speech Services Configuration
speech_key = "3f80ab84124d4539aeef2610dab29da0"
service_region = "eastus2"

connection_string = "DefaultEndpointsProtocol=https;AccountName=caito;AccountKey=o0Qzvj9Z4hWJ0uJwAPMjEEPJt3H6/9LGvm7bwCQKKC1ripO/eLtRQthDTmCbOa+lyFDaLPt4MNKv+AStbNvzPQ==;EndpointSuffix=core.windows.net"
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_name = "caito"  # Replace with the name of your container
container_client = blob_service_client.get_container_client(container_name)
>>>>>>> ab302d1 (Merging autogen from upstream fork.)


def download_audio(video_url, download_path, title, audio_format="wav"):
    """
    Download the audio from a YouTube video URL and convert it to the desired format.

    Parameters:
    video_url (str): The URL of the YouTube video.
    download_path (str): The directory where the downloaded audio will be stored.
    title (str): The desired filename for the downloaded audio.
    audio_format (str): The desired audio format (default is "wav").

    Returns:
    str: The path to the downloaded audio file.
    """
    try:
        yt = YouTube(video_url)
        audio = yt.streams.filter(only_audio=True).first()
        mp4_file_path = os.path.join(download_path, title + ".mp4")
        audio.download(output_path=download_path, filename=title + ".mp4")

        # Convert the downloaded MP4 file to the desired audio format
        audio_file_path = os.path.join(download_path, title + "." + audio_format)
        AudioSegment.from_file(mp4_file_path).export(
            audio_file_path, format=audio_format
        )

        # Clean up the downloaded MP4 file
        os.remove(mp4_file_path)

        return audio_file_path

    except Exception as e:
        print(f"Error downloading {video_url}: {e}")


def transcribe_audio(file_path):
    """
    Transcribe the audio from a file using Azure's Speech to Text API.

    Parameters:
    file_path (str): The path to the audio file.

    Returns:
    str: The transcription text.
    """
    # Set up the speech config
    speech_config = SpeechConfig(subscription=SPEECH_KEY, region=SERVICE_REGION)

    # Set up the audio config
    audio_config = AudioConfig(filename=file_path)

    # Set up the speech recognizer
    recognizer = SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config
    )

    # Use a list to store the transcriptions
    transcriptions = []

    # Define callbacks for the events
    recognizer.recognizing.connect(lambda evt: print(f"RECOGNIZING: {evt.result.text}"))
    recognizer.recognized.connect(lambda evt: transcriptions.append(evt.result.text))

    # Perform the transcription
    recognizer.start_continuous_recognition()

    # Wait for a while for the recognition to finish
    time.sleep(30)

    recognizer.stop_continuous_recognition()

    return " ".join(transcriptions)


def preprocess_transcript(transcript):
    """
    Preprocess the transcript text.

    Parameters:
    transcript (str): The transcript text.

    Returns:
    str: The preprocessed transcript text.
    """
    # Remove punctuation
    transcript = transcript.translate(str.maketrans("", "", string.punctuation))

    # Convert to lowercase
    transcript = transcript.lower()

    return transcript


def create_transcription_job(name, language, content_urls):
    """
    Create a batch transcription job.

    Parameters:
    name (str): The name of the transcription job.
    language (str): The language of the audio data.
    content_urls (list[str]): The URLs of the audio files in Azure Blob Storage.

    Returns:
    dict: The response from the API.
    """
    # Set up the API endpoint
    endpoint = (
        "https://eastus.api.cognitive.microsoft.com/speechtotext/v3.1/transcriptions"
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

    # Make the POST request
    response = requests.post(endpoint, headers=headers, data=json.dumps(body))

    # Check if the request was successful
    if response.status_code != 201:  # 201 Created is the expected status code
        raise Exception(f"Failed to create transcription job: {response.text}")

    # Return the response
    return response.json()


def upload_to_azure(file_path, blob_name):
    """
    Upload a file to Azure Blob Storage.

    Parameters:
    file_path (str): The path to the file to be uploaded.
    blob_name (str): The desired blob name for the uploaded file.

    Returns:
    None
    """
    print(f"Uploading {file_path} to {blob_name}")
    try:
        blob_client = container_client.get_blob_client(blob_name)
        with open(file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)
            print(
                f"File {file_path} uploaded successfully, {os.path.getsize(file_path)} bytes."
            )
    except Exception as e:
        print(f"Error uploading file: {e}")


def main():
    """
    Main function to read a CSV file, download audio, upload the audio to Azure,
    and create a batch transcription job.

    Returns:
    None
    """
    download_dir = "./downloads"

    print(f"Using container: {CONTAINER_NAME}")

    # Create a list to store the URLs of the uploaded audio files
    content_urls = []

    with open("videos.txt") as file:
        reader = csv.DictReader(file)
        for row in reader:
            title = row["Title"]
            url = row["URL"]

            # Download Audio
            print(f"Downloading {title} from {url}")
            audio_file = download_audio(url, download_dir, title)
            print(
                f"Audio file {audio_file} downloaded successfully, {os.path.getsize(audio_file)} bytes."
            )

            # Upload Audio
            print(f"Uploading {title} audio to Azure")
            blob_name = f"audio/{title}.wav"
            upload_to_azure(audio_file, blob_name)
            print(
                f"File {audio_file} uploaded successfully, {os.path.getsize(audio_file)} bytes."
            )

            # Store the URL of the uploaded audio file
            content_urls.append(
                f"https://{ACCOUNT_NAME}.blob.core.windows.net/{CONTAINER_NAME}/{blob_name}"
            )

            # Delete local audio file
            print(f"Deleting local {title} audio file")
            os.remove(audio_file)

    # Create a batch transcription job
    print("Creating batch transcription job")
    create_transcription_job("My Transcription", "en-US", content_urls)


if __name__ == "__main__":
    """
    Entry point of the script.
    """
    main()
