import requests
import json
from datetime import date
from airflow.decorators import task
from airflow.models import Variable

#import os
#from dotenv import load_dotenv
#load_dotenv(dotenv_path="./.env")

API_KEY=Variable.get("API_KEY")
CHANNEL_HANDLE=Variable.get("CHANNEL_HANDLE")
maxResults = 50

@task
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

        return channel_playlistId
    
    except requests.exceptions.RequestException as e:
        raise e

@task
def get_video_ids(playlistId):
    video_ids = []
    pageToken = None
    base_url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&playlistId={playlistId}&key={API_KEY}&maxResults={maxResults}"

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


@task
def extract_video_data(video_ids):
    extracted_data=[]
   
    def batch_list(video_id_list,batch_size):
        # start,stop,step
        for video_id in range(0,len(video_id_list),batch_size):
            # yield -> pauses the function,then resumes again
            yield video_id_list[video_id : video_id + batch_size]#slicing list[start:end]
    
    try:
        for batch in batch_list(video_ids,maxResults):
            video_ids_str = ",".join(batch)
            url = f"https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&id={video_ids_str}&key={API_KEY}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            for item in data.get('items',[]):
                video_id = item['id']
                snippet = item['snippet']
                contentDetails = item['contentDetails']
                statistics = item['statistics']
                video_data={
                    "video_id":video_id,
                    "title":snippet['title'],
                    "publishedAt":snippet['publishedAt'],
                    "duration":contentDetails['duration'],
                    "viewCount":statistics.get('viewCount',None),#if key exists,return value otherwise return default value
                    "likeCount":statistics.get('likeCount',None),
                    "commentCount":statistics.get('commentCount',None),
                }
                extracted_data.append(video_data)
        return extracted_data
            
            
    
    except requests.exceptions.RequestException as e:
        raise e

@task
def save_to_json(extracted_data):
    file_path = f"./data/YT_data_{date.today()}.json"
    with open(file_path,"w",encoding="utf-8") as json_outfile:
        json.dump(extracted_data,json_outfile,indent=4,ensure_ascii=False)


if __name__ == "__main__": #name(library) = main when script is run directly & not imported
    playlist_id = get_playlist_id()
    print(playlist_id)
    video_ids = get_video_ids(playlist_id)
    video_data = extract_video_data(video_ids)
    print(video_data)
    save_to_json(video_data)


