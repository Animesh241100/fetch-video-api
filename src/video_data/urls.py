from django.urls import path
from .views import (
    get_video_list,
    search_query,
)

app_name = 'video_data'

urlpatterns = [
    path('list/', get_video_list),      # listing the fetched video data
    path('search/', search_query),      # the search query api
]