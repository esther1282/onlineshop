from django.shortcuts import render, redirect, get_object_or_404
from shop.models import Product
from .models import Cart, CartItem

def index(request):
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=request.user)
        cart.save()
    return render(request, 'cart/index.html', {'cart': cart})


def addCart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=request.user)
        cart.save()

    try:  # 한번 이미 넣어줬던 경우
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1  # 원하는 수만큼 추가해줘야함 (일단은 +1)
        cart_item.save()
    except CartItem.DoesNotExist:
        # 처음 장바구니에 넣는 상품
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,  # 원하는 수량 (일단은 1)
            cart=cart,
            active=True
        )
        cart_item.save()
    return redirect('cart:index')


def plusCart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart = Cart.objects.get(user=request.user)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart:index')


def minusCart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart = Cart.objects.get(user=request.user)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1 :
        cart_item.quantity -= 1
        cart_item.save()
    return redirect('cart:index')


def deleteCart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart = Cart.objects.get(user=request.user)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart:index')

