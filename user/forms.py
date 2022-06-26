from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']

        widgets = {
            'email': forms.TextInput(attrs={'placeholder': '이메일 주소'}),
            'username': forms.TextInput(attrs={'placeholder': '사용자 이름'}),
            'password1': forms.PasswordInput(attrs={'placeholder': '비밀번호'}),
            'password2': forms.PasswordInput(attrs={'placeholder': '비밀번호확인'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class UpdateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': '사용자 이름'}),
            'password': forms.PasswordInput(attrs={'placeholder': '비밀번호'}),
        }