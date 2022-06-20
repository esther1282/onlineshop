from .models import Product, ProductImage
from django.shortcuts import render, get_object_or_404
from django import forms

def index(request):
    all_products = Product.objects.all()
    user = request.user

    if request.user.is_authenticated is False:
        user.username = ' '
    return render(request, 'shop/index.html', {'all_products': all_products, 'user':user})

def detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    products_images = ProductImage.objects.filter(product=product)
    #quantity = forms.IntegerField(label=1)
    quantity = 1
    return render(request, 'shop/detail.html', {'product': product, 'product_images': products_images})