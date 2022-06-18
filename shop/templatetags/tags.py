from django import template
from shop.models import ProductImage
from django.shortcuts import get_object_or_404

register = template.Library()

@register.filter()
def image_tag(value):
    product_image = get_object_or_404(ProductImage, product=value, is_represent=True)
    if not product_image:
        return "#"
    return product_image.image.url