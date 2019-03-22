from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_friendly_errors.mixins import FriendlyErrorMessagesMixin

from .models import User


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True,
                                  help_text='Unique id of the user. Read only. ')
    username = serializers.CharField(required=True,
                                     validators=[UniqueValidator(queryset=User.objects.all())],
                                     help_text='Unique username.')
    password = serializers.CharField(min_length=6,
                                     write_only=True,
                                     help_text='Password of the user.')
    email = serializers.EmailField(required=True,
                                   validators=[UniqueValidator(queryset=User.objects.all())],
                                   help_text='Email of the user.')
    first_name = serializers.CharField(required=False,
                                       help_text='First name of the user.')
    last_name = serializers.CharField(required=False,
                                      help_text='Last name of the user.')

    is_active = serializers.CharField(read_only=True,
                                      default=False,
                                      help_text='True if user is confirmed. Read only.')
    is_staff = serializers.CharField(read_only=True,
                                     help_text='Email verification status.')

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 'is_active', 'is_staff')

    def validate_password(self, value):
        return make_password(value)

    def validate_email(self, value):
        norm_email = value.lower()
        if User.objects.filter(email=norm_email).exists():
            raise serializers.ValidationError('This field must be unique.')
        return norm_email


class CreatedUserSerializer(FriendlyErrorMessagesMixin, UserSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff')


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(required=True,
                                  help_text='Authorization token.')


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True,
                                     help_text='Unique username.')
    password = serializers.CharField(required=True,
                                     help_text='Password of the user.')


class LoggedInSerializer(serializers.Serializer):
    token = serializers.CharField(help_text='Authentication token of the user.')


class RequestResetPassSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True,
                                   help_text='Email of the user.')


class ResetPassSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True,
                                         min_length=6,
                                         help_text='New password.')


class ResponseSerializer(serializers.Serializer):
    message = serializers.CharField(help_text='Response message.')


class FieldErrorSerializer(serializers.Serializer):
    field = serializers.CharField(help_text='Error in this field.')
    message = serializers.ListField(child=serializers.CharField(),
                                    help_text='Error messages of the field.')


class Error401Serializer(serializers.Serializer):
    detail = serializers.CharField(help_text='Details of authorization failure.')


class Error403Serializer(serializers.Serializer):
    detail = serializers.CharField(help_text='Details of permission failure.')


class ErrorSerializer(serializers.Serializer):
    detail = serializers.CharField(help_text='Details.')


class FriendlyErrorSerializer(serializers.Serializer):
    code = serializers.CharField()
    errors = serializers.ListField(child=ErrorSerializer())
    message = serializers.CharField()
