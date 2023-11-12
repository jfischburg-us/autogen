# filename: video_transcription.py

import os
import subprocess
import speech_recognition as sr
import pandas as pd
import youtube_dl
import json


def transcribe_audio(file):
    r = sr.Recognizer()
    with sr.AudioFile(file) as source:
        audio_data = r.record(source)
        text = r.recognize_google(audio_data)
        return text


def download_youtube_video(url, output):
    ydl_opts = {"format": "bestaudio", "outtmpl": output}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


topics = [
    "Wharton: Scaling a Business: How to Build a Unicorn",
    # limit the number to 5 topics for testing
    "Wharton: Technology Acceleration"
    # more topics here...
]

api_key = "AIzaSyAaFFKKuyFcE4rzIJLkI6aYgEdYDOcTOLE"

output_data = []
for topic in topics:
    print(f"Processing {topic}...")
    query = topic.replace(" ", "+")
    search_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&q={query}&key={api_key}"
    video_info = subprocess.check_output(f"curl {search_url}", shell=True)
    video_info_json = json.loads(video_info)
    items = video_info_json.get("items", [])
    if not items:
        print(f"No video found for topic: {topic}. Skipping...")
        continue
    video_id = items[0]["id"]["videoId"]
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    file_output = f"{topic}.wav"
    download_youtube_video(video_url, file_output)
    transcript = transcribe_audio(file_output)
    os.remove(file_output)
    output_data.append({"topic": topic, "transcript": transcript})

df = pd.DataFrame(output_data)
df.to_csv("transcripts.csv", index=False)
