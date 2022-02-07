from django.urls import path
from .views import (
    get_video_list,
)

app_name = 'video_data'

urlpatterns = [
    path('list/', get_video_list),
    # path('search/', search_view),      # basic search
    # path('opt-search/', optimized_search_view), # optimised search
]