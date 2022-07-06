from datetime import datetime
from django.db import models
from random import choice
from PIL import Image

class Category(models.Model):
    title = models.CharField(max_length=150)
    content = models.CharField(max_length=750)
    def __str__(self):
        return self.title

class Product(models.Model):
    name = models.CharField(max_length=100)
    content = models.TextField(max_length=1000)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField()
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def get_product_image(self):
        try:
            image = self.productimage_set.get(product=self, is_represent=True)
            return image.image.url
        except:
            random_image = choice(ProductImage.objects.filter(product=self))
            return random_image.image.url

def product_image_path(instance, filename):
    return '{}'.format(filename)

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    is_represent = models.BooleanField(default=False)
    image = models.ImageField(upload_to=product_image_path)

    def __str__(self):
        return self.product.name + "'s images"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.height > 400 or img.width > 400:
            output_size = (400, 400)
            img.thumbnail(output_size)
            img.save(self.image.path)


