from django.urls import path
from . import views

app_name = "user"
urlpatterns=[
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('mybag/', views.mybag, name='mybag'),
    path('<int:pk>/', views.profile, name='profile'),
    path('<int:pk>/update/', views.update, name='update'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('logout/', views.logout, name='logout'),
]