from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings
from django.contrib.auth.models import User as auth_user
from django.db.models.signals import post_save
from django.dispatch import receiver

GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('C', 'Custom'),
]

class UserManager(BaseUserManager):
    def _create_user(self, email, username, password, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address.')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username='', password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, username, password, **extra_fields)

    def create_superuser(self, email, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff = True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser = True')

        return self._create_user(email, username, password, **extra_fields)

class User(AbstractUser):
    email = models.EmailField(unique=True, null=False, max_length=255, verbose_name="이메일")
    username = models.CharField(unique=True, null=False, max_length=20, verbose_name="이름")
    phone_number = models.CharField(blank=True, max_length=255, verbose_name="핸드폰")
    address = models.CharField(blank=True, max_length=255, verbose_name="주소")
    gender = models.CharField(blank=True, choices=GENDER_CHOICES, max_length=255)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    #data_joined = models.DateTimeField(verbose_name="date_joined", auto_now_add=True, default='')
    #last_login = models.DateTimeField(verbose_name="last_login", auto_now=True, default='')

    objects = UserManager()

    USERNAME_FIELD = 'email' #email로 구분
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

