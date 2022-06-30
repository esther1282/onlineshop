from django.urls import path
from . import views

app_name = "order"
urlpatterns=[
    path('', views.index, name='index'),
    path('<int:product_id>/', views.order_product, name='order_product'),
    path('cart/', views.order_cart, name='order_cart'),
    path('detail/', views.order_detail, name='order_detail'),
]