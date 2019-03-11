from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework.authtoken.models import Token
from django.core.mail import send_mail
from django.utils import timezone
from django.db import models


class CustomUserManager(UserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        if not email:
            raise ValueError('User must have an email address')

        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):

        if not password:
            raise ValueError('User must have a password')

        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_active') is not True:
            raise ValueError('Superuser must have is_active=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        extra_fields.setdefault('first_name', 'Administrator')
        extra_fields.setdefault('last_name', 'Administrator')
        super_user = self._create_user(username, email, password, **extra_fields)
        Token.objects.create(user=super_user)
        return super_user


class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(max_length=150, unique=True,
                                help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
                                validators=[username_validator],
                                error_messages={'unique': "A user with that username already exists."})

    email = models.EmailField(unique=True, error_messages={'unique': 'A user with that email already exists.'})
    password = models.CharField(max_length=128)

    date_joined = models.DateTimeField(default=timezone.now)

    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=False, help_text='Active status of the user.')
    is_staff = models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.')
    objects = CustomUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_short_name(self):
        return self.first_name

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)
