from rest_framework import serializers

from .models import VoicePost


class VoicePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = VoicePost
        fields = ('name', 'media_file')
