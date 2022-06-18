
from datetime import datetime
from django.db import models

import shop.models


class Category(models.Model):
    title = models.CharField(max_length=150)
    content = models.CharField(max_length=750)
    def __str__(self):
        return self.title

class ImageAlbum(models.Model):

    def represent(self):
        return self.images.get(is_represent=True)


def product_image_path(instance, filename):
    return '{}'.format(filename)


class ProductImage(models.Model):
    is_represent = models.BooleanField(default=False)
    image = models.ImageField(upload_to=product_image_path)
    album = models.ForeignKey(ImageAlbum, related_name='images', on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.product.name + "'s images"



class Product(models.Model):
    name = models.CharField(max_length=100)
    content = models.CharField(max_length=1000)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    album = models.OneToOneField(ImageAlbum, on_delete=models.CASCADE, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name





def clean_is_represent(self):
    product = self.cleaned_data['product']
    is_represent = self.cleaned_data['is_represent']
    if is_represent:
        if ProductImage.objects.filter(product=product, is_represent=True).exists():
            raise forms.ValidationError("Represent image already exists.")
    else:
        if not ProductImage.objects.filter(product=product, is_represent=True).exists():
            raise forms.ValidationError("Please True")
    return is_represent