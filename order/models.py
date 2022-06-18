from django.db import models

class Order(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    shipping = models.FloatField()
    complete = models.BooleanField(default=False)

class OrderItem(models.Model):
    product = models.ForeignKey('shop.Product', on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    date_added = models.DateTimeField(auto_now_add=True)