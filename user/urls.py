from django.urls import path
from . import views

app_name = "user"
urlpatterns=[
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('mybag/', views.mybag, name='mybag'),
    path('mypage/', views.mypage, name='mypage'),
    path('logout/', views.logout, name='logout'),
]