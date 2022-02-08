from django.urls import path
from .views import (
    get_video_list,
    search_query,
    add_api_key,
)

app_name = 'video_data'

urlpatterns = [
    path('list/', get_video_list),      # listing the fetched video data
    path('search/', search_query),      # the search query api
    path('add_v3_key/', add_api_key),      # add a new API key of youtube v3 API
]