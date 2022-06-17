import json

from django.views import View
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth import models, authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from .forms import SignUpForm

@require_http_methods(['GET', 'POST'])
def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('shop:index'))
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

@require_http_methods(['GET', 'POST'])
def signup(request):
    # 로그인되어있다면 회원가입 페이지 접근 막기
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('shop:index'))
    if request.method == 'GET':
        form = SignUpForm()
        return render(request, 'user/signup.html', {'form':form})
    elif request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                form.save()
                user = authenticate(request, email=email, username=username, password=password)

                if user is not None:
                    auth_login(request, user)
                    return HttpResponseRedirect(reverse('shop:index'))
            return render(request, 'user/signup.html', {'form': form})

@login_required
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')
@login_required
def mybag(request):
    return render(request, 'user/mybag.html')
@login_required
def mypage(request):
    return render(request, 'user/mypage.html')
