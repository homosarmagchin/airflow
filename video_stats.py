import json
import requests
import os 
from dotenv import load_dotenv
from datetime import datetime
from airflow.decorators import task

load_dotenv(dotenv_path='.env')

API_KEY = os.getenv('API_KEY')
CHANNEL_HANDLE = os.getenv('CHANNEL_HANDLE')
maxResults = 50
print(f"API_KEY: {API_KEY}")
print(f"CHANNEL_HANDLE: {CHANNEL_HANDLE}")

@task
def get_playlist_id():
    try:
        url = f'https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}'

        response = requests.get(url)
        response.raise_for_status()  

        data = response.json()
        channel_items = data['items'][0]
        channel_playlistId = channel_items['contentDetails']['relatedPlaylists']['uploads']

        print(f"Channel Playlist ID: {channel_playlistId}")

        return channel_playlistId
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
    
def get_video_ids(playlistId):
    video_ids = []
    pageToken = None
    base_url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails,snippet&maxResults={maxResults}&playlistId={playlistId}&key={API_KEY}"
    
    try:
        while True:
            url = base_url

            if pageToken:
                url += f"&pageToken={pageToken}"

            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            print(f"Fetched {len(data.get('items', []))} items from playlist.")

            for item in data.get('items', []):
                video_id = item['contentDetails']['videoId']
                video_ids.append(video_id)

            pageToken = data.get('nextPageToken')

            if not pageToken:
                break
    
        return video_ids
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None    
    

def extract_video_data(video_ids):
    extracted_data = []

    def batch_list(video_id_list, batch_size):
        for id in range(0, len(video_id_list), batch_size):
            yield video_id_list[id:id + batch_size]

    try:
        for batch in batch_list(video_ids, maxResults):
            video_ids_str = ",".join(batch)

            url = f"https://youtube.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id={video_ids_str}&key={API_KEY}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            for item in data.get('items', []):
                video_id = item['id']
                snipped = item['snippet']
                contentDetails = item['contentDetails']
                statistics = item['statistics']
            
                video_data = {
                    "video_id":video_id,
                    "title": snipped.get('title'),
                    "publishedAt": snipped.get('publishedAt'),
                    "duration": contentDetails.get('duration'),
                    "viewCount": statistics.get('viewCount'),
                    "likeCount": statistics.get('likeCount'),
                    "commentCount": statistics.get('commentCount')
                }

                extracted_data.append(video_data)

        return extracted_data
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def save_as_json(extracted_data):
    file_path = f"./data/test_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(extracted_data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    playlistId = get_playlist_id()
    video_ids = get_video_ids(playlistId)
    save_as_json(extract_video_data(video_ids=video_ids))