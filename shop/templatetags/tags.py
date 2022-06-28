from django import template
from random import choice
from ..models import ProductImage
register = template.Library()

@register.filter()
def image_tag(value):
    try:
        product_image = ProductImage.objects.get(product=value, is_represent=True)
        return product_image.image.url
    except:
        random_image = choice(ProductImage.objects.filter(product=value))
        return random_image.image.url

