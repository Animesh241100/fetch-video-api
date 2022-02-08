import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fetch_video.settings")
import django
django.setup()

from googleapiclient.discovery import build
from itertools import cycle
from video_data.models import VideoData


# prepare a circular list of existing API Keys
with open("/code/youtube_api_keys.txt", "r") as fd:      # DOXER
    api_keys = fd.read().splitlines()

api_keys.reverse()
print(api_keys)
api_keys = cycle(api_keys)


# cycle through all the API keys till you find a key for which quota is not exhausted
for api_key in api_keys:
    try: # if any one API key executes successfully, break the loop
        service = build('youtube', 'v3', developerKey=api_key)
        request = service.search().list(
            part='id, snippet',
            q='news',
            type='video',
            order='date',
            maxResults=20,
            publishedAfter='2022-02-07T11:36:09+00:00'
        )
        response = request.execute()  # make request to youtube API
        print(f"Used the API-KEY: {api_key}")
        break
    except Exception as Arg:
        print(f"API-KEY: {api_key} causes exception {Arg}. Skipping to next ...")


# for each and every video data, save it in the database if it doesn't already exist
videos_array = response['items']
for video in videos_array:
    youtube_pk = video['id']['videoId']
    video_data = video['snippet'] 
    try:
        existing_vid = VideoData.objects.get(youtube_pk=youtube_pk)
    except VideoData.DoesNotExist:  # only if no other object with same video_pk exists
        VideoData.objects.create(    # create video objects and save them in database for every response
            youtube_pk = youtube_pk,
            title = video_data['title'],
            description = video_data['description'],
            pub_datetime = video_data['publishedAt'],
            thumbnail_default = video_data['thumbnails']['default']['url'],
            thumbnail_medium = video_data['thumbnails']['medium']['url'],
            thumbnail_high = video_data['thumbnails']['high']['url'],
            channel_title = video_data['channelTitle'],
        )

print("Fetched data from youtube Successfully!!")