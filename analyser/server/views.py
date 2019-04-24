from django.shortcuts import render
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import PictureSerializer
from .picture_mapper import PictureMapper


class PictureUploadView(APIView):
    parser_class = (JSONParser, MultiPartParser,)

    def post(self, request, *args, **kwargs):     
      distance = self.request.GET.get('distance')
      if distance is None:
        return Response('parameter distance is required', status=status.HTTP_400_BAD_REQUEST)

      request.data.update({'distance' : distance})
      file_serializer = PictureSerializer(data=request.data)

      if file_serializer.is_valid():
          picture = file_serializer.save()
          picture_mapper = PictureMapper()
          mapped_objects = picture_mapper.process(picture)
          picture.save()
          print(picture)
          return Response(str(picture), status=status.HTTP_201_CREATED)
      else:
          return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)