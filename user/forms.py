from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User

class SignUpForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']
'''
    def clean(self):
        username = self.cleaned_data('username')
        email = self.cleaned_data('email')
        password1 = self.cleaned_data('password1')
        password2 = self.cleaned_data('password2')
'''

class CustomUserChangeForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['username', 'gender', 'phone_number', 'address']

