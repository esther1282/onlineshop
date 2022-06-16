from .models import Product, ProductImage
from django.shortcuts import render, get_object_or_404

def index(request):
    all_products = Product.objects.all()
    product_image = ProductImage.objects.get(pk=2)

    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = ' '
    return render(request, 'shop/index.html', {'all_products': all_products, 'product_image': product_image, 'username':username})

def detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    products_images = ProductImage.objects.filter(product=product)
    return render(request, 'shop/detail.html', {'product': product, 'product_images': products_images})