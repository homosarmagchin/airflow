import requests
import json
import os

API_KEY = os.getenv('API_KEY')
CHANNEL_HANDLE = os.getenv('CHANNEL_HANDLE')

url = f'https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}'

response = requests.get(url)
print(response)

data = response.json()

print(json.dumps(data, indent=4))


