from rest_framework import serializers

from api.models import Point


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    class Meta:
        model = Point
        fields = ('file',)
