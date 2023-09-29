# filename: get_youtube_videos.py

from googleapiclient.discovery import build
import pandas as pd

api_key = "AIzaSyAaFFKKuyFcE4rzIJLkI6aYgEdYDOcTOLE"  # replace this string with your YouTube API Key

youtube = build("youtube", "v3", developerKey=api_key)

video_info = []

topics = [
    "wharton Scaling a Business: How to Build a Unicorn",
    "wharton Technology Acceleration",
    "wharton Driving Strategic Innovation: Leading Complex Initiatives for Impact",
    "wharton Product Management and Strategy",
    # ... add the rest of the topics similarly, this is kept short for brevity
]

for topic in topics:
    request = youtube.search().list(part="snippet", maxResults=1, q=topic)

    response = request.execute()

    items = response.get("items")
    if items:
        video_info.append(
            [items[0]["snippet"]["title"], f"https://www.youtube.com/watch?v={items[0]['id']['videoId']}"]
        )
    else:
        video_info.append([topic, "http://#"])

df = pd.DataFrame(video_info, columns=["Topic", "URL"])
df.to_csv("wharton_videos.csv", index=False)
