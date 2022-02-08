from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q


from .models import VideoData
from .serializers import VideoDataSerializer


# an api to return the paginated list of the video data currently stored in the database
@api_view(['GET',])
def get_video_list(request):
    paginator = PageNumberPagination()
    video_objects = VideoData.objects.all().order_by('-pub_datetime')
    print(f"LIST: page: {request.GET.get('page', '')}")   # for logging
    result_page = paginator.paginate_queryset(video_objects, request)
    serializer = VideoDataSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


# returns the result of searched query in the database as a response
@api_view(['GET'])
def search_query(request):
    title = request.GET.get('title', '')
    desc = request.GET.get('description', '')
    print(f"SEARCH: title: {title}, description : {desc}")
    if (title ==  '' or desc == ''):        # if any one of the fields are empty, this is against the protocol given in the assignment
        return Response(status=status.HTTP_400_BAD_REQUEST)
    video_objects = VideoData.objects.filter(title=title, description=desc).order_by('-pub_datetime')
    serializer = VideoDataSerializer(video_objects, many=True)
    return Response(serializer.data)



# add a new API key with limits not exhausted
@api_view(['POST'])
def add_api_key(request):
    data = JSONParser().parse(request)
    key = data.get('new_v3_key', '')
    print(f"ADD V3 KEY: new_v3_key: {key}")
    if (key ==  ''):    # don't add the key if it is empty
        return Response(status=status.HTTP_400_BAD_REQUEST)
    try:
        with open("youtube_api_keys.txt", "r") as fd:
            api_keys = fd.read().splitlines()
        print(api_keys)
        if(key not in api_keys):   # Add the key to the list only if it doesn't already exists
            f = open("youtube_api_keys.txt", 'a')
            f.write(key + '\n')
            f.close()
        return Response(status=status.HTTP_201_CREATED)

    except Exception as Arg:
        print("Exception in add_api_key: ", Arg)  # log the exception if occurs
        return Response({"exception" : "An Exception Occured"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# an optimized search query using Indexing on 'title' and 'description' fields of the 'VideoData' (see video_data.models) and Q.OR lookups
@api_view(['GET'])
def optimal_search_query(request):
    paginator = PageNumberPagination()

    # splits the bigger sentence into words
    title = request.GET.get('title', '').split()
    desc = request.GET.get('description', '').split()
    print(title, desc)

    if (title ==  [] and desc == []):  # if both queries are empty, there is nothing to search
        return Response(status=status.HTTP_400_BAD_REQUEST)
    lookup = Q(id__in=[])
    
    # look for the existence of each word in the title and description fields
    for item in title:
        lookup.add(Q(title__icontains=item), Q.OR)
    for item in desc:
        lookup.add(Q(description__icontains=item), Q.OR)
    
    # filter using the prepared lookup
    video_data_objs = VideoData.objects.filter(lookup).order_by('-pub_datetime').distinct()
    result_page = paginator.paginate_queryset(video_data_objs, request)
    serializer = VideoDataSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

