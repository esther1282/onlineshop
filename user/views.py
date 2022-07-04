from django.views import View
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import models, authenticate, get_user_model, login as auth_login, logout as auth_logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from .forms import SignUpForm, CustomUserChangeForm, CheckPasswordForm, CustomPasswordChangeForm

@require_http_methods(['GET', 'POST'])
def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('shop:index'))
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)

        if user is not None:
            auth_login(request, user)
            return HttpResponseRedirect(reverse('shop:index'))
        else:
            return render(request, 'user/login.html', {'context':'로그인 실패'})
    else:
        return render(request, 'user/login.html')

@require_http_methods(['GET', 'POST'])
def signup(request):
    # 로그인되어있다면 회원가입 페이지 접근 막기
    #if request.user.is_authenticated: 템플릿에서 적용하기
    #    return HttpResponseRedirect(reverse('shop:index'))
    if request.method == 'GET':
        form = SignUpForm()
        return render(request, 'user/signup.html', {'form': form})
    elif request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                user = form.save()
                if user is not None:
                    auth_login(request, user)
                    return HttpResponseRedirect(reverse('shop:index'))
            return render(request, 'user/signup.html', {'form': form})

@login_required
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')

@login_required
def profile(request, pk):

    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '업데이트 성공')
            return HttpResponseRedirect(reverse('user:profile', args=[request.user.pk]))
    else:
        form = CustomUserChangeForm(instance=request.user)

    return render(request, 'user/profile.html', {'form':form})

@login_required
def update(request, pk):
    context=''
    if request.method == 'GET':
        form = CustomUserChangeForm(instance=request.user)
    elif request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return render(request, 'user/profile.html', {'form':form})
    return render(request, 'user/update.html', {'form': form, 'context': context})

@require_http_methods(['GET', 'POST'])
@login_required
def delete(request, pk):
    if request.method == 'POST':
        password_form = CheckPasswordForm(request.user, request.POST)

        if password_form.is_valid():
            request.user.delete()
            auth_logout(request)
            return HttpResponseRedirect(reverse('shop:index'))
    else:
        password_form = CheckPasswordForm(request.user)

    return render(request, 'user/delete.html', {'form':password_form})

@require_http_methods(['GET', 'POST'])
@login_required
def change_pw(request, pk):
    if request.method == 'POST':
        password_form = CustomPasswordChangeForm(request.user, request.POST)

        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, '비밀번호를 성공적으로 변경하였습니다.')
            return HttpResponseRedirect(reverse('user:profile', args=[request.user.pk]))
    else:
        password_form = CustomPasswordChangeForm(request.user)

    return render(request, 'user/change_pw.html', {'form':password_form})

