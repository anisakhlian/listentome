from rest_framework import routers
from django.urls import path

from .views import VoicePostViewSet

router = routers.DefaultRouter()
router.register('voice_posts', VoicePostViewSet, basename='voice-posts')

app_name = 'users'
urlpatterns = [
]
