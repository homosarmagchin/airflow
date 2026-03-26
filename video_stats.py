import requests
import json

API_KEY = 'AIzaSyB9j1fn4QvdidfRlHpyg8i0O7Fq9RApXxs'
channel_handle = 'MrBeast'
url = f'https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={channel_handle}&key={API_KEY}'

response = requests.get(url)
print(response)

data = response.json()

print(json.dumps(data, indent=4))


