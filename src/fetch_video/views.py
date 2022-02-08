
from django.shortcuts import render
from video_data.views import get_video_list, optimal_search_query
import json

# returns the default homepage of dashboard
def dashboard_list_view(request):
    video_list = json.loads(json.dumps(get_video_list(request).__dict__["data"]["results"]))  # using the pre-existing api (DRY principle)
    for video in video_list:
        video["videoLink"] = f"https://www.youtube.com/watch?v={video['youtube_pk']}"
    return render(request, 'homepage.html', {"video_list": video_list})

# returns the homepage with the result of a search query
def dashboard_search_view(request):
    video_list = json.loads(json.dumps(optimal_search_query(request).__dict__["data"]["results"])) # using the pre-existing api (DRY principle)
    for video in video_list:
        video["videoLink"] = f"https://www.youtube.com/watch?v={video['youtube_pk']}"
    return render(request, 'homepage.html', {"video_list": video_list})
