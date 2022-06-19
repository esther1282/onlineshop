from django import template
from shop.models import ProductImage
from django.shortcuts import get_object_or_404

register = template.Library()

@register.filter()
def image_tag(value):
    try:
        product_image = ProductImage.objects.get(product=value, is_represent=True)
        return product_image.image.url
    except:
        return "#"