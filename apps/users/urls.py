from rest_framework import routers
from django.urls import path

from .views import SignUpView, ConfirmationView, LoginView, RequestResetPassView, ResetPassView

router = routers.DefaultRouter()

app_name = 'users'
urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('confirmation/<token>/', ConfirmationView.as_view(), name='confirmation'),
    path('login/', LoginView.as_view(), name='login'),
    path('request_reset_pass/', RequestResetPassView.as_view(), name='request-reset-pass'),
    path('reset_pass/', ResetPassView.as_view(), name='reset-pass'),
]
