import requests
import os 
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')

API_KEY = os.getenv('API_KEY')
CHANNEL_HANDLE = os.getenv('CHANNEL_HANDLE')

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
    
if __name__ == "__main__":
    get_playlist_id()
else:
    print("This script is intended to be run directly.")