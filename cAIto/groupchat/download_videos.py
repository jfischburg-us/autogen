import os
import csv
import string
from pytube import YouTube
from pydub import AudioSegment
from azure.storage.blob import BlobServiceClient
from speech_recognition import AudioFile, Recognizer


YOUTUBE_DOMAINS = ["www.youtube.com", "youtu.be"]

# Cognitive/Speech Services Configuration
speech_key = "e6def55c6d904eefa7afe1efa63ac84f"
service_region = "eastus2"

connection_string = "DefaultEndpointsProtocol=https;AccountName=caito;AccountKey=o0Qzvj9Z4hWJ0uJwAPMjEEPJt3H6/9LGvm7bwCQKKC1ripO/eLtRQthDTmCbOa+lyFDaLPt4MNKv+AStbNvzPQ==;EndpointSuffix=core.windows.net"
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_name = "caito"  # Replace with the name of your container
container_client = blob_service_client.get_container_client(container_name)


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
        AudioSegment.from_file(mp4_file_path).export(audio_file_path, format=audio_format)

        # Clean up the downloaded MP4 file
        os.remove(mp4_file_path)

        return audio_file_path

    except Exception as e:
        print(f"Error downloading {video_url}: {e}")


def transcribe_audio(file_path):
    """
    Transcribe the audio from a file using the SpeechRecognition library.

    Parameters:
    file_path (str): The path to the audio file.

    Returns:
    str: The transcription text.
    """
    recognizer = Recognizer()
    with AudioFile(file_path) as source:
        audio = recognizer.record(source)
    transcript = recognizer.recognize_google(audio)
    return transcript


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


def upload_to_azure(file_path, file_name):
    """
    Upload a file to Azure Blob Storage.

    Parameters:
    file_path (str): The path to the file to be uploaded.
    file_name (str): The desired filename for the uploaded file.

    Returns:
    None
    """
    blob_client = container_client.get_blob_client(file_name)
    with open(file_path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)


def main():
    """
    Main function to read a CSV file, download audio, transcribe the audio,
    and prepare the resulting transcripts for training and validation data.

    Returns:
    None
    """
    download_path = "./downloaded_files"

    with open("videos.txt") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            title = row["Title"]
            video_url = row["URL"]

            print(f"Downloading {title} from {video_url}")
            file_path = download_audio(video_url, download_path, title)

            print(f"Transcribing {file_path}")
            transcript = transcribe_audio(file_path)

            # Prepare the transcript for training/validation data
            transcript = preprocess_transcript(transcript)

            # Save the transcript to a text file
            transcript_file_path = os.path.join(download_path, title + ".txt")
            with open(transcript_file_path, "w") as transcript_file:
                transcript_file.write(transcript)

            print(f"Transcript saved to {transcript_file_path}")

            # Upload the transcript file to Azure Blob Storage
            transcript_file_name = "transcripts/" + title + ".txt"
            upload_to_azure(transcript_file_path, transcript_file_name)

            os.remove(file_path)
            os.remove(transcript_file_path)
            print(f"{file_path} and transcript uploaded and local files removed")


if __name__ == "__main__":
    """
    Entry point of the script.
    """
    main()
