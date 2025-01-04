from rest_framework import serializers
from rest_framework.exceptions import ValidationError

# def validate_jpg_string(value):
#     if not value.lower().endswith('.jpeg'):
#         raise ValidationError('String must end with .jpeg')
#     return value

class ImageSerializer(serializers.Serializer):
    designS3Key = serializers.CharField()
    websiteS3Key = serializers.CharField()
