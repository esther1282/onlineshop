from django import forms
from django.contrib.auth.forms import UserChangeForm

from .models import OrderUser

class OrderUserChangeForm(UserChangeForm):
    password = None
    class Meta:
        model = OrderUser
        fields = ['username', 'phone_number', 'address', 'card_number']
