from rest_framework import serializers


class FileUploadSerializer(serializers.Serializer):
    textfile = serializers.FileField(required=True, write_only=True)

