from django.urls import path
from . import views

app_name = "order"
urlpatterns=[
    path('', views.index, name='index'),
    path('create/<int:product_id>', views.create, name='create'),
    path('create/cart', views.create_cart, name='create_cart'),
]