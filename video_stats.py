import requests #pip install requests
import json
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path="./.env")

API_KEY=os.getenv("API_KEY")



CHANNEL_HANDLE = "MrBeast"

def get_playlist_id():
    try:
        #python only replaces variables inside f-strings
        url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}"

        response = requests.get(url)

        #print(response)
        data = response.json()
        
        #print(json.dumps(data,indent=4)) #converts data to json format

        channel_items = data["items"][0]
        channel_playlistId = channel_items["contentDetails"]["relatedPlaylists"]["uploads"]
        print(channel_playlistId)
        return channel_playlistId
    except requests.exceptions.RequestException as e:
        raise e
if __name__ == "__main__": #name(library) = main when script is run directly & not imported
    print("get_playlist_id will be executed.")
    get_playlist_id()
else:
    print("get_playlist_id won't be executed.")

