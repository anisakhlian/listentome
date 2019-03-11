from rest_framework import routers
from django.urls import path

from .views import SignUpView

router = routers.DefaultRouter()

app_name = 'users'
urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
]
