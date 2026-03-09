import requests #pip install requests
import json
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path="./.env")

API_KEY=os.getenv("API_KEY")
maxResults = 50



CHANNEL_HANDLE = "MrBeast"

def get_playlist_id():
    try:
        #python only replaces variables inside f-strings
        url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}"

        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        #print(json.dumps(data,indent=4)) #converts data to json format

        channel_items = data["items"][0]
        channel_playlistId = channel_items["contentDetails"]["relatedPlaylists"]["uploads"]

        print(channel_playlistId)

        return channel_playlistId
    
    except requests.exceptions.RequestException as e:
        raise e


def get_video_ids(playlistId):
    video_ids = []
    pageToken = None
    base_url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&playlistId={playlist_id}&key={API_KEY}&maxResults={maxResults}"

    try:
        while True:
            url = base_url
            if pageToken:
                url+=f"&pageToken={pageToken}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            for item in data.get('items',[]):
                video_id=item['contentDetails']['videoId']
                video_ids.append(video_id)
            pageToken = data.get('nextPageToken')

            if not pageToken:
                break
        return video_ids

    except requests.exceptions.RequestException as e:
        raise e



if __name__ == "__main__": #name(library) = main when script is run directly & not imported
    playlist_id = get_playlist_id()
    print(get_video_ids(playlist_id))
