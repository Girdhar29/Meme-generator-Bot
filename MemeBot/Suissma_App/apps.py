
from rest_framework import serializers

class MemeRequestSerializer(serializers.Serializer):
    prompt = serializers.CharField(max_length=255)

class MemeResponseSerializer(serializers.Serializer):
    image_url = serializers.URLField()
    meme_caption = serializers.CharField()
