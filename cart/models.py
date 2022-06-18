from django.db import models

class Cart(models.Model) :
    user = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True)
    date_added = models.DateField(auto_now_add=True)

class CartItem(models.Model) :
    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    active = models.BooleanField(default = True)