from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.template.loader import render_to_string
from django.core.mail import send_mail
from drf_yasg.utils import swagger_auto_schema
from django.conf import settings

from listentome.front_urls import CONFIRMATION
from .serializers import UserSerializer, CreatedUserSerializer, FieldErrorSerializer


def get_referer(request):
    referer = request.META.get('HTTP_REFERER')
    return referer


class SignUpView(APIView):
    """
    Signs up user.
    """
    serializer_class = UserSerializer

    def get_serializer(self):
        return self.serializer_class()

    @swagger_auto_schema(responses={
        status.HTTP_201_CREATED: CreatedUserSerializer,
        status.HTTP_400_BAD_REQUEST: FieldErrorSerializer,
    })
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.create(user=user)

        message_template = 'user_confirmation.html'
        path = CONFIRMATION.format(token=token.key)

        message = render_to_string(message_template, {
            'user': user,
            'domain': get_referer(request),
            'path': path,
        })
        send_mail('Welcome to Listen2ME!', message, settings.DEFAULT_FROM_EMAIL, [user.email])
        return Response(serializer.data, status=status.HTTP_201_CREATED)
