import requests
import os 
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')

API_KEY = os.getenv('API_KEY')
CHANNEL_HANDLE = os.getenv('CHANNEL_HANDLE')
maxResults = 50


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
    

if __name__ == "__main__":
    playlistId = get_playlist_id()
    video_ids = get_video_ids(playlistId)
    print(video_ids)