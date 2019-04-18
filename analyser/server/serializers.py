from .models import Picture, MappedObject
from rest_framework import serializers


class PictureSerializer(serializers.ModelSerializer):

    class Meta:
        model = Picture
        fields = "__all__"


class MappedObjectSerializer(serializers.Serializer):
	class Meta:
		model = MappedObject
	fields = "__all__"

class MappedObjectsSerializer(serializers.Serializer):
    objects = serializers.ListField(child=MappedObjectSerializer())
