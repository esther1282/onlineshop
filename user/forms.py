from django.contrib.auth import get_user_model
from django import forms

User = get_user_model()

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