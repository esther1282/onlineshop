from django.db import models

class Order(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    shipping = models.FloatField(default=3)
    complete = models.BooleanField(default=False)

    def __str__(self):
        if not self.user:
            return "Anonymous"
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
    product = models.ForeignKey('shop.Product', on_delete=models.DO_NOTHING, null=True)
    quantity = models.IntegerField(default=0)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name+"_order"

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class OrderUser(models.Model):
    email = models.EmailField(unique=True, null=False, max_length=255, verbose_name="이메일")
    username = models.CharField(unique=True, null=False, max_length=20, verbose_name="이름")
    phone_number = models.CharField(null=False, max_length=255, verbose_name="핸드폰")
    address = models.CharField(null=False, max_length=255, verbose_name="주소")
    card_number = models.CharField(null=False, max_length=255, verbose_name="결제카드번호")

    USERNAME_FIELD = 'email'  # email로 구분
    REQUIRED_FIELDS = ['username', 'phone_number', 'address', 'card_number']

    def __str__(self):
        return self.email
