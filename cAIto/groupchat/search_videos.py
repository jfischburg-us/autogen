# filename: search_videos.py

import os
import csv
import googleapiclient.discovery
from googleapiclient.errors import HttpError
import concurrent.futures


def search_videos(youtube, channel, query):
    try:
        search_response = (
            youtube.search()
            .list(q=f"{query} channel:{channel}", type="video", part="id,snippet", maxResults=5)
            .execute()
        )
    except HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred:\n{e.content}")
        return []

    videos = []
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            video_title = search_result["snippet"]["title"]
            video_url = "https://www.youtube.com/watch?v=" + search_result["id"]["videoId"]
            videos.append((video_title, video_url))

    if not videos:
        videos.append((query, "http://#"))

    return videos


def main():
    apiKeyFile = "youtube.txt"
    if not os.path.isfile(apiKeyFile):
        print(f"API key file {apiKeyFile} not found")
        return

    topics = [...]
    channel = "wharton"

    with open(apiKeyFile, "r") as f:
        api_key = f.read().strip()

    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

    with open("video_links.csv", "w", newline="") as csvfile:
        video_writer = csv.writer(csvfile)
        video_writer.writerow(["Title", "URL"])

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {executor.submit(search_videos, youtube, channel, topic): topic for topic in topics}

            for future in concurrent.futures.as_completed(futures):
                topic = futures[future]
                try:
                    videos = future.result()
                    for video in videos:
                        video_writer.writerow(video)
                except Exception as exc:
                    print("%r generated an exception: %s" % (topic, exc))


if __name__ == "__main__":
    main()
