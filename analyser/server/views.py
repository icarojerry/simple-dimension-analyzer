from django.shortcuts import render
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import PictureSerializer


class PictureUploadView(APIView):
    parser_class = (JSONParser, MultiPartParser,)

    def post(self, request, *args, **kwargs):
      print(request.data)
      file_serializer = PictureSerializer(data=request.data)
      
      #print(file_serializer.errors)

      if file_serializer.is_valid():
          file_serializer.save()
          return Response(file_serializer.data, status=status.HTTP_201_CREATED)
      else:
          return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)