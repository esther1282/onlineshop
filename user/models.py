from django.db import models

class User(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('C', 'Custom'),
    ]

    username = models.CharField(blank=True, max_length=255, verbose_name="이름")
    email = models.EmailField(blank=True, max_length=255, verbose_name="이메일")
    password = models.CharField(blank=True, max_length=255, verbose_name="비밀번호")
    phone_number = models.CharField(blank=True, max_length=255)
    address = models.CharField(blank=True, max_length=255)
    #gender = models.CharField(blank=True, choices=GENDER_CHOICES, max_length=255)


    def __str__(self):
        return self.username
