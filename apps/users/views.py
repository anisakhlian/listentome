from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.template.loader import render_to_string
from django.core.mail import send_mail
from drf_yasg.utils import swagger_auto_schema
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate

from listentome.front_urls import CONFIRMATION, RESET_PASS
from .serializers import (UserSerializer, CreatedUserSerializer, FieldErrorSerializer, ResponseSerializer,
                          LoginSerializer, LoggedInSerializer, RequestResetPassSerializer, ResetPassSerializer,
                          Error401Serializer)
from .models import User


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


class ConfirmationView(APIView):
    """
    Confirms registration of corresponding user.
    """

    @swagger_auto_schema(responses={
        status.HTTP_200_OK: ResponseSerializer,
        status.HTTP_404_NOT_FOUND: ResponseSerializer,
    })
    def post(self, request, token):
        user = get_object_or_404(User, auth_token__key=token)
        Token.objects.filter(user=user).update(key=Token().generate_key())

        user.is_active = True
        user.save()
        return Response({'message': 'Registration confirmed.'}, status.HTTP_200_OK)


class LoginView(APIView):
    """
    Authenticates and logs in user with specified credentials.
    """
    serializer_class = LoginSerializer

    def get_serializer(self):
        return self.serializer_class()

    @swagger_auto_schema(responses={
        status.HTTP_200_OK: LoggedInSerializer,
        status.HTTP_404_NOT_FOUND: ResponseSerializer,
    })
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        credentials = {
            'username': serializer.validated_data.get('username'),
            'password': serializer.validated_data.get('password'),
        }
        user = authenticate(**credentials)
        if user:
            token = User.objects.get(username=serializer.validated_data.get('username')).auth_token
            return Response({'token': token.key}, status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid credentials'}, status.HTTP_404_NOT_FOUND)


class RequestResetPassView(APIView):
    """
    Sends email to reset password.
    """
    serializer_class = RequestResetPassSerializer

    def get_serializer(self):
        return self.serializer_class()

    @swagger_auto_schema(responses={
        status.HTTP_200_OK: ResponseSerializer,
        status.HTTP_400_BAD_REQUEST: FieldErrorSerializer,
        status.HTTP_404_NOT_FOUND: ResponseSerializer,
    })
    def post(self, request):
        serializer = RequestResetPassSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User, email=serializer.validated_data['email'])

        message = render_to_string('request_reset_pass.html', {
            'domain': get_referer(request),
            'path': RESET_PASS.format(token=user.auth_token.key),
        })
        send_mail('Reset your password', message, settings.DEFAULT_FROM_EMAIL, [user.email])
        return Response({'message': 'Please check your email to reset the password.'}, status.HTTP_200_OK)


class ResetPassView(APIView):
    """
    Retrieves auth_token from the header. Resets password if authentication was successful.
    To reset password put token from the link in reset password email into the Authorization header.
    """
    serializer_class = ResetPassSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer(self):
        return self.serializer_class()

    @swagger_auto_schema(responses={
        status.HTTP_204_NO_CONTENT: '',
        status.HTTP_400_BAD_REQUEST: FieldErrorSerializer,
        status.HTTP_401_UNAUTHORIZED: Error401Serializer,
    })
    def patch(self, request):
        serializer = ResetPassSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        Token.objects.filter(user=user).update(key=Token().generate_key())
        return Response(status=status.HTTP_204_NO_CONTENT)
