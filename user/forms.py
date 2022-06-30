from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.hashers import check_password
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


class CheckPasswordForm(forms.Form):
    password = forms.CharField(label='비밀번호', widget=forms.PasswordInput(
        attrs={'class': 'form-control', }),
                               )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = self.user.password

        if password:
            if not check_password(password, confirm_password):
                self.add_error('password', '비밀번호가 일치하지 않습니다.')
