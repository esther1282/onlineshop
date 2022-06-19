from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django import forms
from .models import Profile

class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email','username', 'password']

        widgets = {
            'email': forms.TextInput(attrs={'placeholder': '이메일 주소'}),
            'username': forms.TextInput(attrs={'placeholder': '사용자 이름'}),
            'password': forms.PasswordInput(attrs={'placeholder': '비밀번호'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': '사용자 이름'}),
            'password': forms.PasswordInput(attrs={'placeholder': '비밀번호'}),
        }

class UpdateProfileForm(forms.ModelForm):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('C', 'Custom'),
    ]
    class Meta:
        model = Profile
        fields = ['phone_number','address', 'gender']
        widgets = {
            'phone_number': forms.TextInput(attrs={'placeholder': '핸드폰'}),
            'address': forms.TextInput(attrs={'placeholder': '주소'}),
            'gender': forms.TextInput(attrs={'placeholder': '성별'}),
        }