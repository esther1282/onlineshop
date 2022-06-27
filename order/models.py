from django.db import models

class Order(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    shipping = models.FloatField(default=3)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username+"_"+str(self.pk)

    @property
    def get_order_total(self):
        orderitems = self.orderitem_set.all()
        total = 0
        for item in orderitems:
            total += item.get_total
        return total

    @property
    def get_order_items(self):
        return self.orderitem_set.filter(order=self)


class OrderItem(models.Model):
    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=0)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name+"_order"

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total