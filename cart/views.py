from django.shortcuts import render, redirect, get_object_or_404
from shop.models import Product
from .models import Cart, CartItem
from django.http import JsonResponse
from django.http import HttpResponse
import json
from django.core import serializers


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
            each_price=product.price,
            quantity=1,  # 원하는 수량 (일단은 1)
            cart=cart,
            active=True
        )
        cart_item.save()
    if cart.get_cart_total >= 50000:
        cart.shipping = 0
        cart.save()
    return redirect('cart:index')


def plusCart(request):
    if request.is_ajax and request.method == 'POST':
        pk = request.POST.get('pk')
        cartitem = CartItem.objects.get(pk=pk)
        cartitem.quantity +=1
        cartitem.save()

        cart = Cart.objects.get(user=request.user)
        cart_item = CartItem.objects.filter(pk=pk).values()
        total_price = cart.get_cart_total
        if total_price >= 50000:
            cart.shipping = 0
            cart.save()
        context = {'cart_item': list(cart_item), 'total_price': total_price}
        return HttpResponse(json.dumps(context), content_type="application/json")
    else:
        return JsonResponse({'succes': False, 'errors': []}, status=400)


def minusCart(request):
    if request.is_ajax and request.method == 'POST':
        pk = request.POST.get('pk')
        cartitem = CartItem.objects.get(pk=pk)
        if cartitem.quantity > 1:
            cartitem.quantity -= 1
            cartitem.save()

        cart = Cart.objects.get(user=request.user)
        cart_item = CartItem.objects.filter(pk=pk).values()
        total_price = cart.get_cart_total
        if total_price < 50000:
            cart.shipping = 3000
            cart.save()
        context = {'cart_item': list(cart_item), 'total_price': total_price}
        return HttpResponse(json.dumps(context), content_type="application/json")
    else:
        return JsonResponse({'succes': False, 'errors': []}, status=400)


def deleteCart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart = Cart.objects.get(user=request.user)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart:index')

def activeItem(request):
    if request.is_ajax and request.method == 'POST':
        pk = request.POST.get('pk')
        cartitem = CartItem.objects.get(pk=pk)
        cartitem.active = True
        cartitem.save()

        cart = Cart.objects.get(user=request.user)
        total_price = cart.get_cart_total
        if total_price >= 50000:
            cart.shipping = 0
            cart.save()
        context = {'total_price': total_price}
        return HttpResponse(json.dumps(context), content_type="application/json")
    else:
        return JsonResponse({'succes': False, 'errors': []}, status=400)

def disableItem(request):
    if request.is_ajax and request.method == 'POST':
        pk = request.POST.get('pk')
        cartitem = CartItem.objects.get(pk=pk)
        cartitem.active = False
        cartitem.save()

        cart = Cart.objects.get(user=request.user)
        total_price = cart.get_cart_total
        if total_price < 50000:
            cart.shipping = 3000
            cart.save()
        context = {'total_price': total_price}
        return HttpResponse(json.dumps(context), content_type="application/json")
    else:
        return JsonResponse({'succes': False, 'errors': []}, status=400)


