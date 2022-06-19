from django.db import models
from django.conf import settings
from django.contrib.auth.models import User as auth_user
from django.db.models.signals import post_save
from django.dispatch import receiver

class User(models.Model):
    username = models.CharField(blank=True, max_length=255, verbose_name="이름")
    email = models.EmailField(blank=True, max_length=255, verbose_name="이메일")
    password = models.CharField(blank=True, max_length=255, verbose_name="비밀번호")

    def __str__(self):
        return self.username

class Profile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('C', 'Custom'),
    ]
    user = models.OneToOneField(auth_user, default=None, null=True, on_delete=models.CASCADE)
    #user = models.ForeignKey(auth_user, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(blank=True, max_length=255, verbose_name="핸드폰")
    address = models.CharField(blank=True, max_length=255, verbose_name="주소")
    gender = models.CharField(blank=True, choices=GENDER_CHOICES, max_length=255)

    @receiver(post_save, sender=auth_user)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=auth_user)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return self.user #username이 안 뜸
