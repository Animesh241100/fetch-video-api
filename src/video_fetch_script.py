import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fetch_video.settings")
import django
django.setup()

from googleapiclient.discovery import build
from itertools import cycle
from video_data.models import VideoData


with open("youtube_api_keys.txt", "r") as fd:
    api_keys = fd.read().splitlines()

api_keys.reverse()
print(api_keys)
# circular list of API Keys
api_keys = cycle(api_keys)
# api_keys = cycle(['AIzaSyA_kfQA0jeiODALNcuyV6ZSMWx-bUBl7E0', 'AIzaSyCFjgyw53c4AE2nUORVR7IfCsgKReYha8o', 'AIzaSyA_TxCtrqPY2baDTHGo4zzftkw_dcH9JM4', 'AIzaSyBqmw3H4ssowhYX_7kT9O1WbYqrTokgJU0', 'AIzaSyDEU4aWn6ukSqbJzhrKh_09WZlkWsCKpsg', 'AIzaSyCa6lQYPnOVxS4vuofmZlKSoHOsn8_s5rw', 'AIzaSyBWtJZdcLLTtPqGUpeGUzCQ0d_lUAe7HUk'])       # secret key


# cycle through all the API keys in case quota exhausted
for api_key in api_keys:
    try: # if any one API key executes successfully, break the loop and save the data
        service = build('youtube', 'v3', developerKey=api_key)
        request = service.search().list(
            part='id, snippet',
            q='news',
            type='video',
            order='date',
            maxResults=20,
            publishedAfter='2022-02-07T11:36:09+00:00'
        )
        response = request.execute()
        print(f"Used the API-KEY: {api_key}")
        break
    except Exception as Arg:
        print(f"API-KEY: {api_key} causes exception {Arg}. Skipping to next ...")


# api_key = "AIzaSyCa6lQYPnOVxS4vuofmZlKSoHOsn8_s5rw"
# service = build('youtube', 'v3', developerKey=api_key)
# request = service.search().list(
#     part='id, snippet',
#     q='world news',
#     type='video',
#     order='date',
#     maxResults=20,
#     publishedAfter='2022-02-07T11:36:09+00:00'
# )
# # try: # if any one API key executes successfully, break the loop and save the data
# response = request.execute()
# print(f"I worked {api_key}")
#     # break
# # except:
# #     print(f"Limit exhausted switching to other api key: {api_key}")



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
