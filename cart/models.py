from django.db import models

class Cart(models.Model) :
    user = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username+"'s cart"

    @property
    def get_cart_items(self):
        return self.cartitem_set.filter(cart=self)

    @property
    def get_active_items(self):
        return self.cartitem_set.filter(cart=self, active=True)

class CartItem(models.Model) :
    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    active = models.BooleanField(default=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    def __str__(self):
        return self.cart.user.username+"_"+self.product.name