from django.shortcuts import render
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import PictureSerializer


class PictureUploadView(APIView):
    parser_class = (JSONParser, MultiPartParser,)

    def post(self, request, *args, **kwargs):
      file_serializer = PictureSerializer(data=request.data)

      if file_serializer.is_valid():
          #TODO
          #1- get distance from params
          #2- calculate size image and save
          #e.g. file_serializer.distance = request.distance
          #e.g. file_serializer.calculateSize()
          
          file_serializer.save()
          return Response(file_serializer.data, status=status.HTTP_201_CREATED)
      else:
          return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)