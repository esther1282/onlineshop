from django.shortcuts import render, get_object_or_404, redirect
from shop.models import Product, ProductImage
from .models import Order, OrderItem

def index(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'order/index.html', {'orders': orders})

def create(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if product.quantity-1 < 0:
        products_images = ProductImage.objects.filter(product=product)
        return render(request, 'shop/detail.html', {'product': product, 'product_images': products_images, 'error_message': "Sorry, can't order"})
    order = Order.objects.create(user=request.user, shipping=3)
    OrderItem.objects.create(product=product, order=order, quantity=1, price=product.price)

    product.quantity -= 1
    product.save()
    return redirect('order:index')
