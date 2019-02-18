from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser

from .serializers import VoicePostSerializer
from .models import VoicePost


class VoicePostViewSet(ModelViewSet):
    serializer_class = VoicePostSerializer
    http_method_names = ['get', 'post', 'delete']
    parser_classes = (MultiPartParser,)
    queryset = VoicePost.objects.all()

