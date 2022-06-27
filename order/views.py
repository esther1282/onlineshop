from django.shortcuts import render, get_object_or_404, redirect
from shop.models import Product, ProductImage
from .models import Order, OrderItem
from cart.models import Cart

def index(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'order/index.html', {'orders': orders})

def create_cart(request):
    order = empty_order(request)
    cart = Cart.objects.get(user=request.user)
    for item in cart.get_cart_items:
        if item.product.stock - item.quantity < 0:
            return render(request, 'cart/index.html', {'cart': cart, 'error_message': item.product.name+"의 재고가 없습니다"})
    for item in cart.get_cart_items:
        OrderItem.objects.create(product=item.product, order=order, quantity=cart.quantity)
    return redirect('order:index')

def create(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if product.stock-1 < 0:
        products_images = ProductImage.objects.filter(product=product)
        return render(request, 'shop/detail.html', {'product': product, 'product_images': products_images, 'error_message': "Sorry, can't order"})
    order = empty_order(request)
    OrderItem.objects.create(product=product, order=order, quantity=1)

    product.stock -= 1
    product.save()
    return redirect('order:index')

def empty_order(request):
    order = Order.objects.create(user=request.user, shipping=3)
    return order
