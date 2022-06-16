from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout

from .forms import SignUpForm

def login(request):
    if request.method == "GET":
        return render(request, 'user/login.html')
    elif request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return HttpResponseRedirect(reverse('shop:index'))
        else:
            return render(request, 'user/login.html')

def signup(request):
    if request.method == 'GET':
        form = SignUpForm()
        return render(request, 'user/signup.html', {'form':form})
    elif request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth_login(request, user)
                return HttpResponseRedirect(reverse('shop:index'))
        return render(request, 'user/login.html')


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')

def mybag(request):
    return render(request, 'user/mybag.html')
def mypage(request):
    return render(request, 'user/mypage.html')
