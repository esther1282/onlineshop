from django.shortcuts import render, redirect, get_object_or_404
from shop.models import Product
from .models import Cart, CartItem
from django.http import JsonResponse
from django.http import HttpResponse
import json


def index(request):
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=request.user)
        cart.save()

    if request.method == 'POST':
        active_list = request.POST.getlist('active_check')
        cartItems = CartItem.objects.all()
        for item in cartItems:
            if str(item.pk) in active_list:
                item.active = True
                item.save()
            else:
                item.active = False
                item.save()

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


def plusCart(request):
    if request.is_ajax and request.method == 'POST':
        pk = request.POST.get('pk')
        cartitem = CartItem.objects.get(pk=pk)
        cartitem.quantity +=1
        cartitem.save()

        all_item = Cart.objects.get(user=request.user).get_cart_items.values()
        context = {'all_item': list(all_item)}
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

        all_item = Cart.objects.get(user=request.user).get_cart_items.values()
        context = {'all_item': list(all_item)}
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
        return JsonResponse({'succes': True}, status=200)
    else:
        return JsonResponse({'succes': False, 'errors': []}, status=400)

def disableItem(request):
    if request.is_ajax and request.method == 'POST':
        pk = request.POST.get('pk')
        cartitem = CartItem.objects.get(pk=pk)
        cartitem.active = False
        cartitem.save()
        return JsonResponse({'succes': True}, status=200)
    else:
        return JsonResponse({'succes': False, 'errors': []}, status=400)


