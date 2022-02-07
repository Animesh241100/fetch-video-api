from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import VideoData
from .serializers import VideoDataSerializer

# Create your views here.


@api_view(['GET',])
def get_video_list(request):
    paginator = PageNumberPagination()
    video_objects = VideoData.objects.all().order_by('-pub_datetime')
    print(f"LIST: page: {request.GET.get('page', '')}")
    result_page = paginator.paginate_queryset(video_objects, request)
    serializer = VideoDataSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


# returns the result of searched query in the database as a response
@api_view(['GET'])
def search_query(request):
    print(request.GET)
    title = request.GET.get('title', '')
    desc = request.GET.get('description', '')
    print(f"SEARCH: title: {title}, description : {desc}")
    if (title ==  '' or desc == ''):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    video_objects = VideoData.objects.filter(title=title, description=desc).order_by('-pub_datetime')
    serializer = VideoDataSerializer(video_objects, many=True)
    return Response(serializer.data)




