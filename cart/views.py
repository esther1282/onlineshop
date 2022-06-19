from django.shortcuts import render, redirect, get_object_or_404
# from shop.models import Product
# from user.models import User
#from .models import Cart, CartItem

def index(request):
    return render(request, 'cart/index.html')


def addCart(request, product_id):
    #product = Product.objects.get(pk=product_id)
    """if not request.user.is_authenticated:
        return render(request, 'shop/index.html', {'error_message': 'First Login please'})

    user = request.user
    try:
        cart = Cart.objects.get(user=user)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            user=user
        )
        cart.save()

    try: # 한번 이미 넣어줬던 경우
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1 # 원하는 수만큼 추가해줘야함 (일단은 +1)
        cart_item.save()
    except CartItem.DoesNotExist:
        # 처음 장바구니에 넣는 상품
        cart_item = CartItem.objects.create(
            product=product,
            quantity = 1,# 원하는 수량 (일단은 1)
            cart=cart,
            active= True
        )
        cart_item.save()
"""
    return redirect('cart:index')
